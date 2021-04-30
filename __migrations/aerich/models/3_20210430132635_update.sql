-- upgrade --
ALTER TABLE "____sub_module_storage_atlant_nsi_basicclient_organizationsrf" RENAME COLUMN "INN777" TO "INN888";
-- downgrade --
ALTER TABLE "____sub_module_storage_atlant_nsi_basicclient_organizationsrf" RENAME COLUMN "INN888" TO "INN777";
