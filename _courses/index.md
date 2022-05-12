---
layout: page
title: Workshops and Courses
---
{% for course in site.courses %}

{% if course.hidden %}

  {% comment %} Checking if item.field is NIL isn't supported before Jekyll 4.0... {% endcomment %}

{% else %}
  {% include course-overview-box.html title=course.name %}

  <table class="training-courses"><tr>
  <td class="course-title" id="{{ course.name | slugify }}">
    <span class="course-name">{{ course.name }}</span>
    <br>
    {% if course.type %}
    {{ course.type }}<br>
    {% endif %}
    {% if course.subtitle %}
    <i>{{ course.subtitle }}</i><br>
    {% endif %}
  </td>
  </tr><tr>
  <td class="course-content">{{ course.content | markdownify }}</td>
  </tr><tr>
  <td class="course-upcoming-date">
    {% if course.materials-link %}
    {% include button.html text="Course Materials" link=course.materials-link %}
    {% endif %}

    {% if course.page-link %}
    {% include button.html text="Course Page" link=course.page-link %}
    {% endif %}

    {% if course.signup-link %}
    {% include button.html text="Sign Up" link=course.signup-link %}
    {% endif %}
    <br>
    Next Session: {{ course.upcoming-date }}
  </td>
  </tr></table>
  <br>

{% endif %}

{% endfor %}
