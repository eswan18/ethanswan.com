---
layout: page
title: Workshops and Courses
---

{% for course in site.courses %}

{% if course.hidden %}

  {% comment %} Checking if item.field is NIL isn't supported before Jekyll 4.0... {% endcomment %}

{% else %}

  <table class="training-courses"><tr>
  <td class="course-name" id="{{ course.name | slugify }}">
    {% if course.type %}
    <h6>{{ course.type }}</h6>
    {% endif %}
    <h4>{{ course.name }}</h4>
    {% if course.subtitle %}
    <br><i>{{ course.subtitle }}</i>
    {% endif %}
  </td>
  </tr><tr>
  <td class="course-content">{{ course.content | markdownify }}</td>
  </tr><tr>
  <td class="course-upcoming-date">
    {% if course.materials-link %}
    {% include button.html text="Link to Materials" link=course.materials-link icon="github" %}
    <br>
    {% endif %}
    {% if course.page-link %}
    {% include button.html text="Course Page" link=course.page-link %}
    <br>
    {% endif %}
    Next Session: {{ course.upcoming-date }}
  </td>
  </tr></table>
  <br>

{% endif %}

{% endfor %}
