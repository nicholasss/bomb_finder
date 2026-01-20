from tile_sprite import TileSprite


def calculate_neighbors(
    center_tile: tuple[int, int],
    grid_cols: int,
    grid_rows: int,
    grid: list[list[TileSprite]],
) -> int:
    """
    Counts the bombs surrounding the tile in the center.
    """
    number_of_bombs = 0
    center_col, center_row = center_tile

    for col in range(-1, 2):
        for row in range(-1, 2):
            # iterate through the surrounding tiles
            tile_col, tile_row = center_col + col, center_row + row

            # skip looking at the center tile itself
            if col == 0 and row == 0:
                continue

            # check if tile is too low outside grid
            elif tile_col < 0 or tile_row < 0:
                continue

            # check if tile is too high outside grid
            elif tile_col >= grid_cols or tile_row >= grid_rows:
                continue

            # check for bomb
            if grid[tile_col][tile_row].has_bomb():
                number_of_bombs += 1

    # print(f"tile {center_tile} as {number_of_bombs} bombs")
    return number_of_bombs
