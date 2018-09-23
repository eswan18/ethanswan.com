---
layout: coffee_shops
title: Ethan Swan - Coffee Shops
---

# Coffee Shops

Ranking Cincinnati coffee shops has allowed me to pursue 2 of my favorite hobbies: visiting local cafés and complaining about things.
The following are arranged in alphabetical order.
<br><br>

<table>
<!--Headers-->
<tr>
<th>Coffee Shop</th>
<th>Description</th>
<th>Accepts Apple Pay</th>
<th>WiFi Quality</th>
<th>Rating (0-9)</th>
</tr>
<!--One row per coffee shop-->
{% for shop in site.coffee_shops %}
<tr>
    {% if shop.link %}
        <td><a href="{{ shop.link }}">{{ shop.name }}</a></td>
    {% else %}
        <td>{{ shop.name }}</td>
    {% endif %}
    <!--The content comes in with <p> tags that mess up formatting. Remove-->
    {% assign newcontent=shop.content | markdownify | replace: '<p>', '' %}
    {% assign newcontent=newcontent | replace: '</p>', '' %}
    <td>{{ newcontent }}</td>
    <td>{{ shop.apple_pay }}</td>
    <td>{{ shop.wifi }}</td>
    <td>{{ shop.rating }}</td>
</tr>
{% endfor %}
</table>
