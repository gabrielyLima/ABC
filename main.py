import fitness
import food_source
from ABC import ABC


def main():
    best_cost = []
    execution = 3
    for j in range(execution):
        print(j)
        abc_sphere = ABC(npopulation=30, nruns=400, fn_eval=fitness.rosenbrock, fn_lb=[(-30) for _ in range(30)],
                         fn_ub=[(30) for _ in range(30)])

        x = abc_sphere.optimize(fitness.rosenbrock)
        eval_result = fitness.rosenbrock(x)
        best_cost.append(abc_sphere.food_source_history)
        print(f'Sphere MIN: x={x}')
        print(f'Sphere({x}) = {round(eval_result, 4)}')
    print(best_cost)

    avg_cost = []
    for i in range(237):
        sum = 0
        for j in range(execution):
            sum += best_cost[j][i]
        media = sum/execution
        avg_cost.append(media)
    print(avg_cost)

    for y in range(len(avg_cost)):
        arquivo = open("ABC_RastriginFunction.txt", "a")
        arquivo.writelines(str(avg_cost[y]) + ", ")

if __name__ == '__main__':
    main()