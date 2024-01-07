#
# (c) 2024, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from mybody_api_client.utils.base_section import ApiException

from app.utils import google_sheets_api_client, mybody_api_client
from config import TABLE_NAME


async def create_other():
    table = await google_sheets_api_client.get_table_by_name(name=TABLE_NAME)

    async def create_roles():
        try:
            await mybody_api_client.client.role.get(id_=1)
        except ApiException:
            role_id = await mybody_api_client.admin.role.create(name='Root')
            await mybody_api_client.admin.account.create_role(account_id=1, role_id=role_id)

    async def create_permissions():
        sheet = await google_sheets_api_client.get_sheet_by_table_and_name(table=table, name='permissions')
        rows = await google_sheets_api_client.get_rows(sheet=sheet)
        permissions = [permission.id_str for permission in await mybody_api_client.client.permission.get_list()]

        for row in rows:
            permission = row.id_str
            name = row.name
            if permission in permissions:
                continue

            await mybody_api_client.admin.permission.create(id_str=permission, name=name)
            await mybody_api_client.admin.role.create_permission(role_id=1, permission=permission)

    async def create_texts():
        sheet = await google_sheets_api_client.get_sheet_by_table_and_name(table=table, name='texts')
        rows = await google_sheets_api_client.get_rows(sheet=sheet)
        texts_keys = [permission.key for permission in await mybody_api_client.admin.text.get_list()]

        for row in rows:
            key = row.key
            value_default = row.value_default
            if key in texts_keys:
                continue

            await mybody_api_client.admin.text.create(key=key, value_default=value_default)

    await create_roles()
    await create_permissions()
    await create_texts()