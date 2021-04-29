-- upgrade --
CREATE TABLE IF NOT EXISTS "____sub_module_storage_atlant_nsi_basicclient_organizationsrf" (
    "INN777" VARCHAR(100) NOT NULL  PRIMARY KEY,
    "OKTMO" VARCHAR(100) NOT NULL
);
COMMENT ON COLUMN "____sub_module_storage_atlant_nsi_basicclient_organizationsrf"."INN777" IS 'ИНН';
COMMENT ON COLUMN "____sub_module_storage_atlant_nsi_basicclient_organizationsrf"."OKTMO" IS 'OKTMO';
COMMENT ON TABLE "____sub_module_storage_atlant_nsi_basicclient_organizationsrf" IS 'супер инфа';
-- downgrade --
DROP TABLE IF EXISTS "____sub_module_storage_atlant_nsi_basicclient_organizationsrf";
