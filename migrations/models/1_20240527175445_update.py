from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "password" VARCHAR(128) NOT NULL;
        ALTER TABLE "user" ADD "email" VARCHAR(254) NOT NULL;
        ALTER TABLE "user" ALTER COLUMN "first_name" DROP NOT NULL;
        ALTER TABLE "user" ALTER COLUMN "last_name" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP COLUMN "password";
        ALTER TABLE "user" DROP COLUMN "email";
        ALTER TABLE "user" ALTER COLUMN "first_name" SET NOT NULL;
        ALTER TABLE "user" ALTER COLUMN "last_name" SET NOT NULL;"""
