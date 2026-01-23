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
            if grid[tile_col][tile_row].has_bomb:
                number_of_bombs += 1

    # print(f"tile {center_tile} as {number_of_bombs} bombs")
    return number_of_bombs


def click_to_tile_coord(
    click_coord: tuple[int, int],
    grid_topleft: tuple[int, int],
    tile_render_size: tuple[int, int],
) -> tuple[int, int]:
    """
    Converts screen coordinates to tile grid coordinates.
    """

    # Unpacking tuples
    click_x, click_y = click_coord
    grid_left, grid_top = grid_topleft
    tile_width, tile_height = tile_render_size

    # Click position relative to the tile grid
    rel_click_x, rel_click_y = (
        click_x - grid_left,
        click_y - grid_top,
    )

    # Floor divide the click position to find the tile coordinates
    tile_col, tile_row = (
        rel_click_x // tile_width,
        rel_click_y // tile_height,
    )

    return (tile_col, tile_row)


def click_was_inside_grid(
    tile_clicked: tuple[int, int], grid_size: tuple[int, int]
) -> bool:
    """
    Will provide a boolean to indicate whether the tile that was clicked, was inside the grid or not.
    This calculation assumes that the first argument, tile_clicked, has already converted to a (col, row) value.

    Useful to prevent IndexErrors when accessing elements in a matrix directly.
    """

    # Unpacking tuples
    tile_clicked_col, tile_clicked_row = tile_clicked
    grid_cols, grid_rows = grid_size

    # Is outside grid?
    if tile_clicked_col < 0 or tile_clicked_row < 0:
        return False
    elif tile_clicked_col >= grid_cols or tile_clicked_row >= grid_rows:
        return False

    # If not, then it is inside the grid
    return True
