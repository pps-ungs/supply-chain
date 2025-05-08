select * 
from public.experimentos_x_inicial
where (x_inicial, y_inicial, y_optimo) in (
	select x_inicial, y_inicial, max(y_optimo) as y_optimo
	from public.experimentos_x_inicial
	group by x_inicial, y_inicial
) order by x_inicial, cant_iteraciones