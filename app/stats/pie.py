import uuid

import matplotlib.pyplot as plt

from app.config import settings
from app.tasks.constants import TASK_STATUSES
from app.tasks.schemas import TaskStatus


def paint_pie_plot(stats: dict[TaskStatus, int], *, title: str = "Total tasks: {count}") -> str:
    # Разделяем классы и их количество для построения графика
    class_names = [TASK_STATUSES[status]["text"] for status in stats.keys()]
    class_values = list(stats.values())

    # Получаем цвета
    colors = [TASK_STATUSES[status]["color"] for status in stats.keys()]

    # Строим круговую диаграмму
    plt.figure()
    my_circle = plt.Circle((0, 0), 0.8, color="white")
    plt.pie(class_values, labels=class_names, autopct="%.0f%%", colors=colors)

    p = plt.gcf()
    p.gca().add_artist(my_circle)
    plt.title(title.format(count=sum(class_values)))
    pie_path = f"{settings.stats.stats_dir}/pie_{uuid.uuid4().hex}.png"
    plt.savefig(pie_path)
    plt.close()

    return pie_path
