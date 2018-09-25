<h3>Tea Web Scraping</h3>
<p>
Scrapy project for scraping various high-quality tea ecommerce sites.
Extracts the type of tea (Green, White, Pu'Erh, etc.), the origin
(China, Yunnan Province, Japan, etc.) and any images associated with the product.
Using sites listed here: https://specialtyteaalliance.org/world-of-tea/no-bullshit/,
as well as any others I find suitable.
</p><br/><p>
Changing the image destination dir: IMAGES_STORE parameter in the RunSpiders.py file\n
Destination for the rest of the data: OUT_PATH param in WritingPipeline class in the pipelines.py file
</p><br/><p>
To use, run 'python <path-to-file>/RunSpiders.py'
</p><br/><p>
Sites included so far:
TeaSpring\n
Asha Teahouse\n
ESGreen\n
Mei Leaf\n
Ippodo\n
</p>
