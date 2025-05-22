select * from public.experimentos_hill_climbing order by obj desc;

--mejores por estrategia
select * 
from public.experimentos_hill_climbing 
where (estrategia, obj) in (
	select estrategia, max(obj) obj
	from public.experimentos_hill_climbing
	group by estrategia
)
order by obj desc


select 
	coalesce(malos.estrategia, regulares.estrategia, buenos.estrategia) estrategia, 
	coalesce(cant_malos, 0) cant_malos, 
	coalesce(cant_regulares, 0) cant_regulares, 
	coalesce(cant_buenos, 0) cant_buenos 
from (
	--cant malos por estrategia
	select estrategia, count(*) cant_malos
	from public.experimentos_hill_climbing
	where obj < 1469054.372
	group by estrategia
) as malos

full join (
	--cant regulares por estrategia
	select estrategia, count(*) cant_regulares
	from public.experimentos_hill_climbing
	where obj >= 1469054.372 and obj < 2938108.744
	group by estrategia
) as regulares
on malos.estrategia = regulares.estrategia

full join (
	--cant buenos por estrategia
	select estrategia, count(*) cant_buenos
	from public.experimentos_hill_climbing
	where obj >= 2938108.744
	group by estrategia
) as buenos
on regulares.estrategia = buenos.estrategia
order by cant_buenos desc, cant_regulares desc, cant_malos desc