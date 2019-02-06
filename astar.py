
class Node():
    # Klasa pola

    # Konstruktor dla klasy pól
    def __init__(self, parent=None, position=None, weight=0, direction =1):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
        self.w = weight
        self.direction = direction

    # Porównanie wartości
    def __eq__(self, other):
        return self.position == other.position

    def set_w(self, w):
        self.w = w

def check_direction(current_diretion):

    if current_diretion == 1:
        directions = 1, 2, 3, 4, -1, 0
    if current_diretion == 2:
        directions = 2, 1, 3, 4, 0, 1
    if current_diretion == 3:
        directions = 3, 1, 2, 4, 0, -1
    if current_diretion == 4:
        directions = 4, 1, 2, 3, 1, 0
    return directions


def astar(maze, start, end):
    # Zwraca liste krotek jako ścieżkę od startu do pola końcowego (Wybrana struktura to krotka, ponieważ nie można jej zmienić)

    # Tworzymy początkowy i końcowy punkt
    # print(maze[4][4])
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Tworzymy dwie listy pomocnicze, otwarte scieżki i zamknięte(te użyte)
    open_list = []
    closed_list = []

    # Dodajemy to otwartych punkt startowy
    open_list.append(start_node)

    # Główna pętla to znalezienia odpowiedniej ścieżki (jak nie znajdzie, zwraca pustą listę) Sprawdza dopóki są niezbadane ścieżki
    while len(open_list) > 0:

        # Weź aktualne pole
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:                      #TU porównujemy
                current_node = item
                current_index = index

        # Wyrzuć aktualne pole z listy otwartych ścieżek i dodaj do listy zamkniętych
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Jeśli znaleźliśmy drogę
        if current_node == end_node:
            sum = 0
            path = []
            current = current_node
            while current is not None:
                sum += current.w
                path.append(current.position)
                current = current.parent

            #print(sum)
            return path[::-1] # Zwraca ścieżkę, znaleziono drogę!

        # Generujemy sąsiednie pola, na które możemy przejść
        children = []

        directions = check_direction(current_node.direction)
        for new_position in [(directions[4], directions[5], directions[0]), (0, 0, directions[1]), (0, 0, directions[2]), (0, 0, directions[3])]: # Dodajemy cztery pola w każdą ze stron

            # Ustalamy pozycję pola
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1], new_position[2])

            # Sprawdzamy, czy nie wyszliśmy poza mapę
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

             # Upewniamy się, że mozemy się poruszać po polu
            if maze[node_position[0]][node_position[1]] == -1:
                continue

             # Zapewnia brak zapętlania się algorytmu w przypadku, gdy nie można znaleźć ścieżki
            if Node(current_node, node_position) in closed_list:
                continue

              # Jeśli wszystko okej, twprzymy kolejne pole
            new_node = Node(current_node, node_position,maze[node_position[0]][node_position[1]],new_position[2])

            children.append(new_node)

        # Pętla po wszystkich sąsiednich polach (dzieciach) głównego pola
        for child in children:

            # Jeśli sąsiednie pole (dziekco pola aktualnego) jest na liscie użytych pól
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Tworzymy F, G i H do obliczania wagi pola (G-łączna waga od startowego pola, H-łączna waga do końcowego pola, F-suma wag G i H)
            child.g = current_node.g + current_node.w # Waga od startowego pola
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2) #H wyliczamy heurystycznie z twierdzenia pitagorasa a^2 + b^2 = c^2
            child.f = child.g + child.h # Suma dwóch poprzednich

            # Jeśli sąsiednie pole (dziecko) jest na liście otwartych pól
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Dodaj pole sąsaida na listę otwartych pól
            open_list.append(child)

