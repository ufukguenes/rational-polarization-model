from manim import *
import Statistics

stats_of_run = None


def visualise(stats):
    global stats_of_run
    stats_of_run = stats
    BasicAnimation().render()


class BasicAnimation(Scene):
    global stats_of_run


    def construct(self):

        this_stats = stats_of_run
        print("Number of frames: " + str(len(this_stats.agents_over_time)))
        number_of_agents = len(this_stats.agents_over_time[0])
        agents_as_circles = []
        for i in range(number_of_agents):
            agents_as_circles.append(Circle().set_fill(BLUE, opacity=0.5))

        self.play(*apply_copy(agents_as_circles, Create))

        apply_return(agents_as_circles, animate_this)

        apply_return(agents_as_circles, scale_elem)
        self.play(*agents_as_circles)

        init_step = True
        for index in range(len(this_stats.average_opinion)):
            step_coord = []
            if not init_step:
                for agents_opinion in this_stats.average_opinion[index]:
                    step_coord.append(agents_opinion)
                init_step = False
                apply_return(agents_as_circles, apply_Xcoord, param=step_coord)
                self.play(*agents_as_circles)
            else:
                for agents_opinion in this_stats.average_opinion[0]:
                    step_coord.append([0, agents_opinion])
                init_step = False

                apply_return(agents_as_circles, apply_2Dcoord, param=step_coord)
                self.play(*agents_as_circles)


def animate_this(elem):
    return elem.animate


def scale_elem(elem):
    return elem.scale(0.2)

def apply_2Dcoord(elem, coordinates):
    for index in range(len(coordinates)):
        elem.set_coord(coordinates[index], index)
    return elem


def apply_Ycoord(elem, y_coord):
    elem.set_coord(y_coord, 1)
    return elem


def apply_Xcoord(elem, x_coord):
    elem.set_coord(x_coord, 0)
    return elem


def apply_return(arr, func, param=[]):
    if len(param) == len(arr):
        for index in range(len(arr)):
            arr[index] = func(arr[index], param[index])
    else:
        for index in range(len(arr)):
            arr[index] = func(arr[index])


def apply_copy(arr, func, param=[]):
    return_arr = []
    if len(param) == len(arr):
        for index in range(len(arr)):
            return_arr.append(func(arr[index], param[index]))
    else:
        for index in range(len(arr)):
            return_arr.append(func(arr[index]))

    return return_arr
