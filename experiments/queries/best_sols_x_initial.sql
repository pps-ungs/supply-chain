--maximos x
select * 
from public.experimentos_x_inicial
where (x_inicial, y_inicial, y_optimo) in (
	select x_inicial, y_inicial, max(y_optimo) as y_optimo
	from public.experimentos_x_inicial
	group by x_inicial, y_inicial
) order by x_inicial, cant_iteraciones

--mejor resultado por step por x inicial
select *
from public.experimentos_x_inicial
where (x_inicial, y_inicial, step, y_optimo) in (
	select x_inicial, y_inicial, step, max(y_optimo) as y_optimo
	from public.experimentos_x_inicial
	group by step, x_inicial, y_inicial
)

--mejor resultado por cant_iteraciones por x inicial
select *
from public.experimentos_x_inicial
where (x_inicial, y_inicial, y_optimo, cant_iteraciones) in (
	select x_inicial, y_inicial, max(y_optimo) as y_optimo, cant_iteraciones
	from public.experimentos_x_inicial
	group by cant_iteraciones, x_inicial, y_inicial
)

--peores resultados por step
select * 
from public.experimentos_x_inicial
where (step, y_optimo) in (
	select step, min(y_optimo) as peor_y
	from public.experimentos_x_inicial
	group by step
) order by step, y_optimo

--mejor resultado por estrategia
select * 
from public.experimentos_x_inicial
where (estrategia, y_optimo) in (
	select estrategia, max(y_optimo) as y_optimo
	from public.experimentos_x_inicial
	group by estrategia
) order by estrategia, y_optimo, cant_iteraciones