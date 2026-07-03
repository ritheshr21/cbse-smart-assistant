class WeaknessTracker:
    def __init__(self):
        self.topic_mistakes = {}

    def update(self, topic, is_correct):
        if not is_correct:
            self.topic_mistakes[topic] = self.topic_mistakes.get(topic, 0) + 1

    def get_weak_topics(self):
        return sorted(
            [
                {"topic": topic, "mistakes": count}
                for topic, count in self.topic_mistakes.items()
            ],
            key=lambda x: x["mistakes"],
            reverse=True
        )

    def get_suggestions(self):
        suggestions = []

        for topic, count in self.topic_mistakes.items():
            if count >= 2:
                suggestions.append(f"Revise {topic} (high mistakes)")
            else:
                suggestions.append(f"Practice more questions on {topic}")

        return suggestions