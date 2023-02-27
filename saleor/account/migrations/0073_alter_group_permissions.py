# Generated by Django 3.2.16 on 2022-12-06 10:06

from django.db import migrations, models

# Forward helpers
DROP_OLD_CONSTRAINTS = """
ALTER TABLE account_group_permissions
    DROP CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;

ALTER TABLE account_group_permissions
    DROP CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;

ALTER TABLE account_group_permissions
    DROP CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq;

ALTER TABLE account_user_groups
    DROP CONSTRAINT userprofile_user_groups_group_id_c7eec74e_fk_auth_group_id;

ALTER TABLE account_user_user_permissions
    DROP CONSTRAINT userprofile_user_use_permission_id_1caa8a71_fk_auth_perm;
"""

CREATE_NEW_CONSTRAINTS = """
ALTER TABLE account_group_permissions
    ADD CONSTRAINT account_group_permissions_group_id_permission_id_745742e5_uniq
    UNIQUE (group_id, permission_id);

ALTER TABLE account_group_permissions
    ADD CONSTRAINT account_group_permissions_group_id_37f7fcd9_fk_account_group_id
    FOREIGN KEY (group_id) REFERENCES account_group (id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE account_group_permissions
    ADD CONSTRAINT account_group_permis_permission_id_f654f978_fk_permissio
    FOREIGN KEY (permission_id) REFERENCES permission_permission (id)
    DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE account_user_groups
    ADD CONSTRAINT account_user_groups_group_id_6c71f749_fk_account_group_id
    FOREIGN KEY (group_id) REFERENCES account_group (id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE account_user_user_permissions
    ADD CONSTRAINT account_user_user_pe_permission_id_66c44191_fk_permissio
    FOREIGN KEY (permission_id) REFERENCES permission_permission (id)
    DEFERRABLE INITIALLY DEFERRED;
"""

RENAME_CONSTRAINTS_AND_INDEX = """
ALTER TABLE account_group_permissions
    RENAME CONSTRAINT auth_group_permissions_pkey
    TO account_group_permissions_pkey;

ALTER INDEX IF EXISTS auth_group_permissions_group_id_b120cbf9
    RENAME TO account_group_permissions_group_id_37f7fcd9;

ALTER INDEX IF EXISTS auth_group_permissions_permission_id_84c5c92e
    RENAME TO account_group_permissions_permission_id_f654f978;
"""

# Reverse helpers
CREATE_NEW_CONSTRAINTS_REVERSE = """
ALTER TABLE account_group_permissions
    DROP CONSTRAINT account_group_permis_permission_id_f654f978_fk_permissio;

ALTER TABLE account_group_permissions
    DROP CONSTRAINT account_group_permissions_group_id_37f7fcd9_fk_account_group_id;

ALTER TABLE account_group_permissions
    DROP CONSTRAINT account_group_permissions_group_id_permission_id_745742e5_uniq;

ALTER TABLE account_user_groups
    DROP CONSTRAINT account_user_groups_group_id_6c71f749_fk_account_group_id;

ALTER TABLE account_user_user_permissions
    DROP CONSTRAINT account_user_user_pe_permission_id_66c44191_fk_permissio;
"""

RENAME_CONSTRAINTS_AND_INDEX_REVERSE = """
ALTER TABLE account_group_permissions
    RENAME CONSTRAINT account_group_permissions_pkey
    TO auth_group_permissions_pkey;

ALTER INDEX IF EXISTS account_group_permissions_group_id_37f7fcd9
    RENAME TO auth_group_permissions_group_id_b120cbf9;

ALTER INDEX IF EXISTS account_group_permissions_permission_id_f654f978
    RENAME TO auth_group_permissions_permission_id_84c5c92e;
"""


class Migration(migrations.Migration):
    dependencies = [
        ("permission", "0001_initial"),
        ("account", "0072_group"),
        ("app", "0018_auto_20221122_1148"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                # Those constraints should be reverted after rename table in 0072.
                migrations.RunSQL(
                    DROP_OLD_CONSTRAINTS, reverse_sql=migrations.RunSQL.noop
                ),
                migrations.RunSQL(
                    CREATE_NEW_CONSTRAINTS, reverse_sql=CREATE_NEW_CONSTRAINTS_REVERSE
                ),
                migrations.RunSQL(
                    RENAME_CONSTRAINTS_AND_INDEX,
                    reverse_sql=RENAME_CONSTRAINTS_AND_INDEX_REVERSE,
                ),
            ],
            state_operations=[
                migrations.AlterField(
                    model_name="group",
                    name="permissions",
                    field=models.ManyToManyField(
                        blank=True,
                        to="permission.Permission",
                        verbose_name="permissions",
                    ),
                ),
                migrations.AlterField(
                    model_name="user",
                    name="groups",
                    field=models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",  # noqa: E501
                        related_name="user_set",
                        related_query_name="user",
                        to="account.Group",
                        verbose_name="groups",
                    ),
                ),
                migrations.AlterField(
                    model_name="user",
                    name="user_permissions",
                    field=models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="permission.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
        ),
    ]