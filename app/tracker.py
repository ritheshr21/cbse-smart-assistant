class WeaknessTracker:
    def __init__(self):
        self.weak_topics = {}

    def update(self, topic, is_correct):
        if not is_correct:
            self.weak_topics[topic] = self.weak_topics.get(topic, 0) + 1

    def get_weak_topics(self):
        return sorted(self.weak_topics.items(), key=lambda x: x[1], reverse=True)