---
layout: page
title: Training
---


{% for course in site.courses %}
<table class="training-courses"><tr>
<td class="course-name">{{ course.name }}</td>
</tr><tr>
<td class="course-content">{{ course.content | markdownify }}</td>
</tr><tr>
<td class="course-upcoming-date">Next Session: {{ course.upcoming-date }}</td>
</tr></table>
<br>
{% endfor %}
