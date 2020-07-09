---
layout: page
title: "Coffee Shop Ratings: Chicago"
city: Chicago
aside-type: coffee-shops
---

I moved to Chicago in the summer of 2020, and that brought a lot of life changes.
One thing that hasn't changed is my habit of visiting and critiquing coffee shops.

The following are arranged from highest- to lowest-rated.
<br><br>

{% assign shops = site.coffee_shops | where:"city","Chicago" | sort: 'rating' %}
{% for shop in shops reversed %}
<div class="coffee-shop" id="{{ shop.name | slugify }}">
<table>
<tr>
<th colspan="3">
    {% if shop.link %}
        <h3><b><a href="{{ shop.link }}">{{ shop.name }}</a></b></h3>
    {% else %}
        <h3>{{ shop.name }}</h3>
    {% endif %}
</th>
</tr><tr>
<td colspan="3" class="coffee-shop-desc">
    <!--The content comes in with <p> tags that mess up formatting. Remove-->
    {% assign newcontent=shop.content | markdownify | replace: '<p>', '' %}
    {% assign newcontent=newcontent | replace: '</p>', '' %}
    {{ newcontent }}
</td>
</tr><tr>
<td class="coffee-shop-attr">
  <span class="coffee-shop-attr-name">
    Apple Pay
  </span>
  <br>
  <span class="coffee-shop-attr-value">
    {% if shop.apple_pay %}Yes{% else %}No{% endif %}
  </span>
</td>
<td class="coffee-shop-attr">
  <span class="coffee-shop-attr-name">
    WiFi
  </span>
  <br>
  <span class="coffee-shop-attr-value">
    {{ shop.wifi }}
  </span>
</td>
<td class="coffee-shop-attr">
  <span class="coffee-shop-attr-name">
    Overall Rating
  </span>
  <br>
  <span class="coffee-shop-attr-value">
    {{ shop.rating }}
  </span>
</td>
</tr>
</table>
</div>
{% endfor %}
<br>
