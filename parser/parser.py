from argparse import ArgumentParser
from pathlib import Path
import asyncio

import asyncpg
import aiofiles
from bs4 import BeautifulSoup
from aiohttp import client


BASE_URL = 'https://calorizator.ru/'


BASE_DIR = Path(__file__).parent

STATIC_DIR = BASE_DIR.parent / 'static' / 'product'

if not STATIC_DIR.exists():
    STATIC_DIR.mkdir()


parser = ArgumentParser()

parser.add_argument('--database-url', type=str)

args = parser.parse_args()


async def parse_products(session: client.ClientSession, db: asyncpg.Connection, page: int):
    async with session.get(f'/product/all?page={page}') as response:
        response_html = await response.text()
        soup = BeautifulSoup(response_html, 'html.parser')
        products = soup.select('tr.odd, tr.even')
        print(f"Parsing {len(products)} products on {page} page")
        for product in products:
            links = product.select('a')
            title = (links[1] if len(links) == 2 else links[0]).text
            print(f"Parsing {title}")
            existing_products = await db.fetch('SELECT title FROM products WHERE title = $1', title)
            if existing_products:
                return

            photo_url = links[0].select('img')[0].get('src') if len(links) == 2 else None
            photo_url = photo_url.replace('/24/', '/product_512/') if photo_url else None
            if photo_url:
                filename = photo_url.split('/')[-1]
                get_url = photo_url.replace('https://calorizator.ru/', '/')
                if not (STATIC_DIR / filename).exists():
                    async with session.get(get_url) as response:
                        f = await aiofiles.open(STATIC_DIR / filename, 'wb')
                        await f.write(await response.read())

                file_url = f"/static/product/{filename}"
            else:
                file_url = None

            kkal = float(product.select('.views-field-field-kcal-value')[0].text.strip() or '0')
            await db.execute('INSERT INTO products (title, title_vector, kkal, file_url) VALUES ($1, to_tsvector($1::varchar), $2, $3);', title, kkal, file_url)


async def main():
    conn: asyncpg.Connection = await asyncpg.connect(args.database_url)
    await conn.execute('CREATE TABLE IF NOT EXISTS products ('
                       '  id SERIAL PRIMARY KEY,'
                       '  title VARCHAR(255),'
                       '  title_vector tsvector,'
                       '  kkal REAL,'
                       '  file_url VARCHAR(500)'
                       ');')
    await conn.execute('CREATE INDEX IF NOT EXISTS products_title_search ON products USING gin(title_vector)')
    async with client.ClientSession(BASE_URL) as session:
        for i in range(83):
            await parse_products(session, conn, i)

        count: str | None = await conn.fetchval('SELECT COUNT(*) FROM products;')
        assert count
        print(f"Fetched products count: {count}")


if __name__ == '__main__':
    asyncio.run(main())
