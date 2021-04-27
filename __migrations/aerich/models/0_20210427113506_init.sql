-- upgrade --
CREATE TABLE IF NOT EXISTS "____sub_module_storage_atlant_aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "____sub_module_storage_atlant_example_tortoise_orm" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL
);
COMMENT ON TABLE "____sub_module_storage_atlant_example_tortoise_orm" IS 'Example model';
