import random
import string
from typing import Dict, List


class PasswordGenerator:
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    def generate_password(
        self,
        length: int = 12,
        use_uppercase: bool = True,
        use_lowercase: bool = True,
        use_digits: bool = True,
        use_special: bool = True,
    ) -> str:
        if length < 4:
            length = 4

        char_sets = []
        all_chars = ""

        if use_lowercase:
            char_sets.append(self.lowercase)
            all_chars += self.lowercase
        if use_uppercase:
            char_sets.append(self.uppercase)
            all_chars += self.uppercase
        if use_digits:
            char_sets.append(self.digits)
            all_chars += self.digits
        if use_special:
            char_sets.append(self.special_chars)
            all_chars += self.special_chars

        if not char_sets:
            char_sets = [self.lowercase]
            all_chars = self.lowercase

        # Гарантируем наличие хотя бы одного символа из каждой выбранной категории
        password = []
        for char_set in char_sets:
            password.append(random.choice(char_set))

        # Заполняем оставшиеся символы
        for _ in range(length - len(password)):
            password.append(random.choice(all_chars))

        # Перемешиваем
        random.shuffle(password)
        return "".join(password)

    def generate_multiple_passwords(self, count: int = 5, **kwargs) -> List[str]:
        return [self.generate_password(**kwargs) for _ in range(count)]

    def check_password_strength(self, password: str) -> Dict[str, any]:
        score = 0
        feedback = []

        if len(password) >= 8:
            score += 1
        else:
            feedback.append("Пароль должен быть не менее 8 символов")

        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append("Добавьте строчные буквы")

        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("Добавьте заглавные буквы")

        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("Добавьте цифры")

        if any(c in self.special_chars for c in password):
            score += 1
        else:
            feedback.append("Добавьте специальные символы")

        strength_levels = {
            0: "Очень слабый",
            1: "Слабый",
            2: "Умеренный",
            3: "Хороший",
            4: "Сильный",
            5: "Очень сильный",
        }

        return {
            "score": score,
            "strength": strength_levels[score],
            "feedback": feedback,
        }
