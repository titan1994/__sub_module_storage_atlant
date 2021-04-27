-- upgrade --
CREATE TABLE IF NOT EXISTS "____sub_module_storage_atlant_nsi_general_nsi_new_dict" (
    "INN777" VARCHAR(100) NOT NULL  PRIMARY KEY,
    "OKTMO" VARCHAR(100) NOT NULL
);
COMMENT ON COLUMN "____sub_module_storage_atlant_nsi_general_nsi_new_dict"."INN777" IS 'ИНН';
COMMENT ON COLUMN "____sub_module_storage_atlant_nsi_general_nsi_new_dict"."OKTMO" IS 'OKTMO';
COMMENT ON TABLE "____sub_module_storage_atlant_nsi_general_nsi_new_dict" IS 'супер инфа';
-- downgrade --
DROP TABLE IF EXISTS "____sub_module_storage_atlant_nsi_general_nsi_new_dict";
