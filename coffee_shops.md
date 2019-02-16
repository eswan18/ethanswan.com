---
layout: coffee_shops
title: Ethan Swan - Coffee Shops
---

# Cincinnati Coffee Shops

Ranking local coffee shops has allowed me to pursue two of my favorite hobbies: visiting cafés and complaining about things.

The following are arranged from highest- to lowest-rated.
<br><br>

<table>
<!--Headers-->
<tr>
<th>Coffee Shop</th>
<th>Description</th>
<th>Accepts Apple Pay</th>
<th>WiFi Quality</th>
<th>Rating (0-10)</th>
</tr>
<!--One row per coffee shop-->
{% assign shops = site.coffee_shops | sort: 'rating' %}
{% for shop in shops reversed %}
<tr>
    {% if shop.link %}
        <td><b><a href="{{ shop.link }}">{{ shop.name }}</a></b></td>
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
