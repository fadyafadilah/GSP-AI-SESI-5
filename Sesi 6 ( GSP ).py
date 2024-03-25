class Block:
    def __init__(self, name):
        self.name = name
        self.on = None
        self.clear = True

    def put_on(self, block):
        self.on = block
        self.clear = False

    def remove_from(self):
        self.on = None
        self.clear = True

    def __str__(self):
        return self.name


class Arm:
    def __init__(self):
        self.holding = None

    def pick_up(self, block):
        self.holding = block

    def put_down(self):
        block = self.holding
        self.holding = None
        return block

    def __str__(self):
        return "Arm"


class TowerOfBlocks:
    def __init__(self, blocks):
        self.blocks = blocks
        self.arm = Arm()

    def unstack(self, block):
        if block.on and block.clear and self.arm.holding is None:
            self.arm.pick_up(block)
            block.on.remove_from()
            return True
        return False

    def stack(self, block):
        if self.arm.holding and block.clear:
            self.arm.holding.put_on(block)
            return True
        return False

    def put_down(self):
        if self.arm.holding:
            block = self.arm.put_down()
            return block
        return None

    def is_goal_state(self, goal_state):
        for goal_block in goal_state:
            if goal_block.on is None:
                if not self.blocks[goal_block.name].clear:
                    return False
            else:
                if self.blocks[goal_block.name].on != self.blocks[goal_block.on.name]:
                    return False
        return True

    def solve(self, goal_state):
        actions = []
        for goal_block in goal_state:
            if not self.blocks[goal_block.name].clear:
                actions.append("UNSTACK({},{})".format(self.blocks[goal_block.name].on, goal_block.name))
                self.unstack(self.blocks[goal_block.name])
            if self.arm.holding == self.blocks[goal_block.name]:
                actions.append("PUTDOWN({})".format(goal_block.name))
                block = self.put_down()
                if block:
                    if block.on:
                        actions.append("STACK({}, {})".format(block.name, block.on.name))
                        self.stack(self.blocks[block.name])
                    else:
                        actions.append("STACK({}, ONTABLE)".format(block.name))
                        self.stack(self.blocks[block.name])
            else:
                if self.blocks[goal_block.name].clear:
                    actions.append("PICKUP({})".format(goal_block.name))
                    self.arm.pick_up(self.blocks[goal_block.name])
                    if goal_block.on:
                        actions.append("STACK({}, {})".format(goal_block.name, goal_block.on.name))
                        self.stack(self.blocks[goal_block.name])
                    else:
                        actions.append("STACK({}, ONTABLE)".format(goal_block.name))
                        self.stack(self.blocks[goal_block.name])
        return actions




def main():
    blocks = {
        "A": Block("A"),
        "B": Block("B"),
        "C": Block("C"),
        "D": Block("D"),
        "E": Block("E"),
        "F": Block("F"),
        "G": Block("G"),
        "H": Block("H"),
        "I": Block("I"),
        "J": Block("J")
    }

    initial_state = [blocks["B"], blocks["A"], blocks["D"], blocks["C"], blocks["F"], blocks["E"], blocks["H"],
                     blocks["G"], blocks["J"], blocks["I"]]
    goal_state = [blocks["A"], blocks["B"], blocks["C"], blocks["D"], blocks["E"], blocks["F"], blocks["G"],
                  blocks["H"], blocks["I"], blocks["J"]]

    tower = TowerOfBlocks(blocks)

    actions = tower.solve(goal_state)

    print("Solution:")
    for action in actions:
        print(action)


if __name__ == "__main__":
    main()
