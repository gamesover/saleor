# Generated by Django 4.2.15 on 2024-10-23 11:43
from decimal import Decimal

from babel.numbers import get_currency_precision
from django.db import migrations
from django.db.models import OuterRef
from prices import Money

BATCH_SIZE = 2000


def queryset_in_batches(queryset):
    """Slice a queryset into batches.

    Input queryset should be sorted be pk.
    """
    start_pk = 0

    while True:
        qs = queryset.filter(pk__gt=start_pk)[:BATCH_SIZE]
        pks = list(qs.values_list("pk", flat=True))
        if not pks:
            break
        yield pks
        start_pk = pks[-1]


def quantize_price(price: Money, currency: str) -> Money:
    precision = get_currency_precision(currency)
    number_places = Decimal(10) ** -precision
    return price.quantize(number_places)


def propagate_lines_undiscounted_unit_price(apps, _schema_editor):
    CheckoutLine = apps.get_model("checkout", "CheckoutLine")
    TaxConfiguration = apps.get_model("tax", "TaxConfiguration")
    ProductVariantChannelListing = apps.get_model(
        "product", "ProductVariantChannelListing"
    )
    checkout_lines = CheckoutLine.objects.filter(
        undiscounted_unit_price_amount__isnull=True
    ).order_by("pk")
    for pks in queryset_in_batches(checkout_lines):
        lines = (
            CheckoutLine.objects.select_related("checkout")
            .annotate(
                listing_price=ProductVariantChannelListing.objects.filter(
                    variant_id=OuterRef("variant_id"),
                    channel_id=OuterRef("checkout__channel_id"),
                ).values_list("price_amount", flat=True)
            )
            .filter(pk__in=pks, undiscounted_unit_price_amount__isnull=True)
        )
        channel_ids = {line.checkout.channel_id for line in lines}
        tax_configurations = TaxConfiguration.objects.filter(
            channel_id__in=channel_ids
        ).values_list("channel_id", "prices_entered_with_tax")
        channel_id_to_prices_with_tax_map = dict(tax_configurations)

        for line in lines:
            if line.listing_price is not None:
                line.undiscounted_unit_price_amount = line.listing_price
                continue

            channel_id = line.checkout.channel_id
            if channel_id_to_prices_with_tax_map.get(channel_id):
                base_total_price = line.total_price_gross_amount
            else:
                base_total_price = line.total_price_net_amount

            if base_total_price is Decimal(0) or line.quantity == 0:
                line.undiscounted_unit_price_amount = Decimal(0)
            else:
                line.undiscounted_unit_price_amount = quantize_price(
                    base_total_price / line.quantity, line.currency
                )
        CheckoutLine.objects.bulk_update(lines, ["undiscounted_unit_price_amount"])


class Migration(migrations.Migration):
    dependencies = [
        ("tax", "0008_auto_20240122_1353"),
        ("product", "0194_auto_20240620_1404"),
        ("checkout", "0070_checkoutline_undiscounted_unit_price_amount"),
    ]

    operations = [
        migrations.RunPython(
            propagate_lines_undiscounted_unit_price,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
