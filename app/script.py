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


from app.utils import mybody_api_client
from config import USERNAME, PASSWORD, FIRSTNAME, LASTNAME, SURNAME


async def run_script():
    languages = await mybody_api_client.client.language.get_list()
    if not len(languages.languages):
        mybody_api_client.admin.language.create(id_str='eng', name='English')

    timezones = await mybody_api_client.client.timezone.get_list()
    if not len(timezones.timezones):
        mybody_api_client.admin.timezone.create(id_str='utc', deviation=0)

    currencies = await mybody_api_client.client.currency.get_list()
    if not len(currencies.currencies):
        mybody_api_client.admin.currency.create(id_str='usd')

    countries = await mybody_api_client.client.country.get_list()
    if not len(countries.countries):
        mybody_api_client.admin.country.create(
            id_str='usd',
            name='United States',
            language='eng',
            timezone='utc',
            currency='usd',
        )

    have_account = await mybody_api_client.client.account.check_username(username=USERNAME)
    if have_account['state'] == 'successful':
        await mybody_api_client.client.account.create(
            username=USERNAME,
            password=PASSWORD,
            firstname=FIRSTNAME,
            lastname=LASTNAME,
            surname=SURNAME,
            country='usa',
            language='eng',
            timezone='utc',
            currency='usd',
        )
