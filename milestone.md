
# {{ milestone.title }}
Scheduled for: {{ milestone.due_on }}

{{ milestone.description }}

{% if not verbose %}
## Issues
{% else %}
## Summary
{% endif %}
{% for repo, values in issues.iteritems() %}
### {{ repo.name }}
{% for issue in values %}
* {% if issue.state == "closed" %}~~{{ issue.title }}~~{% else %}{{ issue.title }}{% endif %} **[{{ issue.assignee.login }}]**
{% endfor %}
{% endfor %}
{% if verbose %}

## Detailed Descriptions
{% for repo, values in issues.iteritems() %}
### {{ repo.name }}
  {% for issue in values %}
#### {% if issue.state == "closed" %}~~{{ issue.title }}~~{% else %}{{ issue.title }}{% endif %} **[{{ issue.assignee.login }}]**  

{{ issue.body }}
***
{% endfor %}
{% endfor %}
{% endif %}
