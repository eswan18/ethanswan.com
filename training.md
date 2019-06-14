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
  {% if course.materials-link %}
  {% include button.html text="Link to Materials" link=course.materials-link %}
  <br>
  {% endif %}
  Next Session: {{ course.upcoming-date }}
</td>
</tr></table>
<br>
{% endfor %}
