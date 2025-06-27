--maximos obj
select * 
from public.experimento_hill_climbing
where (x_inicial, obj_inicial, obj) in (
	select x_inicial, obj_inicial, max(obj) as obj
	from public.experimento_hill_climbing
	group by x_inicial, obj_inicial
) order by obj desc, cant_iteraciones

--mejor resultado por step por x inicial
select *
from public.experimento_hill_climbing
where (x_inicial, obj_inicial, step, obj) in (
	select x_inicial, obj_inicial, step, max(obj) as obj
	from public.experimento_hill_climbing
	group by step, x_inicial, obj_inicial
)
order by step, obj desc

--mejor resultado por cant_iteraciones por x inicial
select *
from public.experimento_hill_climbing
where (x_inicial, obj_inicial, obj, cant_iteraciones) in (
	select x_inicial, obj_inicial, max(obj) as obj, cant_iteraciones
	from public.experimento_hill_climbing
	group by cant_iteraciones, x_inicial, obj_inicial
) 
order by cant_iteraciones, obj desc

--peores resultados por step
select * 
from public.experimento_hill_climbing
where (step, obj) in (
	select step, min(obj) as peor_obj
	from public.experimento_hill_climbing
	group by step
)
order by step, obj

--mejor resultado por estrategia
select * 
from public.experimento_hill_climbing
where (estrategia, obj) in (
	select estrategia, max(obj) as obj
	from public.experimento_hill_climbing
	group by estrategia
) order by estrategia, obj desc, cant_iteraciones