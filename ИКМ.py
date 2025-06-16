'''
Для заданного подмножества набора костей домино определить, можно ли их
выложить в ряд, не нарушая правил. Если можно, то представить один любой
вариант такого разложения. Например, для входных данных 31, 00, 13,
получаем ответ: некорректные входные данные; для входных данных 02, 04,
42 ответ: можно, 04, 42, 20. Использовать двухсвязный список.
'''


class DominoTile:
    def __init__(self, value_left: int, value_right: int) -> None:
        """
        Args:
            value_left (int): Левая часть кости.
            value_right (int): Правая часть кости.
        """
        self.value_left = value_left
        self.value_right = value_right

    def flip(self) -> None:
        """Меняет местами левую и правую часть кости."""
        self.value_left, self.value_right = self.value_right, self.value_left

    def clone(self) -> "DominoTile":
        """
        Returns:
            DominoTile: Копия текущей кости.
        """
        return DominoTile(self.value_left, self.value_right)

    def __str__(self) -> str:
        """
        Returns:
            str: Строка вида '24' (кость 2|4).
        """
        return str(self.value_left) + str(self.value_right)


class DominoNode:
    def __init__(self, tile: DominoTile) -> None:
        """
        Args:
            tile (DominoTile): Кость, хранящаяся в этом узле.
        """
        self.tile = tile
        self.prev_node: DominoNode | None = None
        self.next_node: DominoNode | None = None


class DominoLinkedChain:
    def __init__(self) -> None:
        """Создаёт пустую цепочку домино."""
        self.node_first: DominoNode | None = None
        self.node_last: DominoNode | None = None

    def append_tile(self, tile: DominoTile) -> None:
        """
        Добавляет кость в конец цепочки.

        Args:
            tile (DominoTile): Кость, которую нужно добавить.
        """
        node = DominoNode(tile)
        if self.node_last:
            self.node_last.next_node = node
            node.prev_node = self.node_last
            self.node_last = node
        else:
            self.node_first = self.node_last = node

    def to_list(self) -> list[str]:
        """
        Returns:
            list[str]: Список костей в строковом виде.
        """
        result = []
        current = self.node_first
        while current:
            result.append(str(current.tile))
            current = current.next_node
        return result

    @staticmethod
    def build_if_possible(tiles: list[DominoTile]) -> "DominoLinkedChain | None":
        """
        Пытается построить цепочку из набора костей.
        Возвращает цепочку или None, если построить нельзя.

        Args:
            tiles (list[DominoTile]): Список костей.

        Returns:
            DominoLinkedChain | None: Построенная цепочка или None.
        """
        def generate_permutations(tiles: list[DominoTile]) -> list[list[DominoTile]]:
            """
            Генерирует все перестановки костей.

            Args:
                tiles (list[DominoTile]): Исходные кости.

            Returns:
                list[list[DominoTile]]: Все перестановки костей.
            """
            result: list[list[DominoTile]] = []

            def permute(start: int) -> None:
                if start == len(tiles):
                    result.append([tile.clone() for tile in tiles])
                    return
                for i in range(start, len(tiles)):
                    tiles[start], tiles[i] = tiles[i], tiles[start]
                    permute(start + 1)
                    tiles[start], tiles[i] = tiles[i], tiles[start]

            permute(0)
            return result

        def generate_flips(tiles: list[DominoTile]) -> list[list[DominoTile]]:
            """
            Генерирует все комбинации поворотов костей.

            Args:
                tiles (list[DominoTile]): Перестановка костей.

            Returns:
                list[list[DominoTile]]: Все комбинации с поворотами.
            """
            result: list[list[DominoTile]] = []

            def flip(index: int) -> None:
                if index == len(tiles):
                    result.append([tile.clone() for tile in tiles])
                    return
                flip(index + 1)
                tiles[index].flip()
                flip(index + 1)
                tiles[index].flip()

            flip(0)
            return result

        def is_valid_chain(tiles: list[DominoTile]) -> bool:
            """
            Проверяет, образуют ли кости правильную цепочку.

            Args:
                tiles (list[DominoTile]): Список костей.

            Returns:
                bool: True, если цепочка допустима.
            """
            for i in range(len(tiles) - 1):
                if tiles[i].value_right != tiles[i + 1].value_left:
                    return False
            return True

        for permutation in generate_permutations(tiles):
            for variant in generate_flips(permutation):
                if is_valid_chain(variant):
                    chain = DominoLinkedChain()
                    for tile in variant:
                        chain.append_tile(tile)
                    return chain
        return None


def main() -> None:
    """Основной пользовательский интерфейс."""
    print("Домино — обработка списков костей")
    all_inputs: list[str] = []

    while True:
        print("\nМеню:")
        print("1 – Добавить список костей")
        print("2 – Показать ранее введённые списки")
        print("3 – Выход")

        try:
            command = input("Выберите действие: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nПрограмма остановлена вручную.")
            break

        if command == "1":
            while True:
                try:
                    print("Введите кости через запятую (например: 02, 04, 42):")
                    input_str = input(">>> ").strip()
                except (KeyboardInterrupt, EOFError):
                    print("\nПрограмма остановлена вручную.")
                    return

                if not input_str:
                    print("error: no tiles to check")
                    continue

                parts = [s.strip() for s in input_str.split(",")]
                tiles: list[DominoTile] = []
                valid = True

                for part in parts:
                    if len(part) != 2 or not part.isdigit():
                        print("error: input must contain exactly two digits (e.g., 02)")
                        valid = False
                        break
                    a = int(part[0])
                    b = int(part[1])
                    if a > 6 or b > 6:
                        print("error: domino values must be between 0 and 6")
                        valid = False
                        break
                    tiles.append(DominoTile(a, b))

                if not valid:
                    continue

                all_inputs.append(input_str)
                chain = DominoLinkedChain.build_if_possible(tiles)
                if chain:
                    print("Можно:", ", ".join(chain.to_list()))
                else:
                    print("Нельзя.")
                break

        elif command == "2":
            if not all_inputs:
                print("Списки не введены.")
            else:
                print("Ранее введённые списки:")
                for i, entry in enumerate(all_inputs, 1):
                    print(f"{i}) {entry}")

        elif command == "3":
            print("Программа завершена.")
            break
        else:
            print("error: unknown command")


if __name__ == "__main__":
    main()
