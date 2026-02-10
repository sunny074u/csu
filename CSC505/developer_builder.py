class Developer:
    def __init__(self, curiosity, empathy, adaptability):
        self.curiosity = curiosity
        self.empathy = empathy
        self.adaptability = adaptability

    def describe_traits(self):
        print("Building your ideal developer...\n")
        print(f"Trait: Curiosity – {self.curiosity}")
        print(f"Trait: Empathy – {self.empathy}")
        print(f"Trait: Adaptability – {self.adaptability}")
        print("\nTotal traits included: 3")


class DeveloperBuilder:
    def __init__(self):
        self.curiosity = None
        self.empathy = None
        self.adaptability = None

    def set_curiosity(self, description):
        self.curiosity = description
        return self

    def set_empathy(self, description):
        self.empathy = description
        return self

    def set_adaptability(self, description):
        self.adaptability = description
        return self

    def build(self):
        return Developer(
            curiosity=self.curiosity,
            empathy=self.empathy,
            adaptability=self.adaptability
        )


if __name__ == "__main__":
    builder = DeveloperBuilder()

    developer = (
        builder
        .set_curiosity("Drives exploration of new tools and techniques")
        .set_empathy("Enhances team communication and user understanding")
        .set_adaptability("Enables flexibility in changing environments")
        .build()
    )

    developer.describe_traits()
