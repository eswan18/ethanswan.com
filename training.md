---
layout: page
title: Training
---


{% for course in site.courses %}
<table class="training-courses"><tr>
<td class="course-name">
  <h4>{{ course.name }}</h4>
  {% if course.subtitle %}
  <br><i>{{ course.subtitle }}</i>
  {% endif %}
</td>
</tr><tr>
<td class="course-content">{{ course.content | markdownify }}</td>
</tr><tr>
<td class="course-upcoming-date">
  Next Session: {{ course.upcoming-date }}
  {% if course.materials-link %}
  <br><a href="{{ course.materials-link }}" target="_blank">Link to Materials</a>
  {% endif %}
</td>
</tr></table>
<br>
{% endfor %}
