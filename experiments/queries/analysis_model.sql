select * from public.experimento_hill_climbing
where experimento = '100_it_all_x'
order by obj desc;

--mejores por experimento, estrategia
select *
from public.experimento_hill_climbing
where experimento = '100_it_all_x' and (experimento, estrategia, obj) in (
	select experimento, estrategia, max(obj) obj
	from public.experimento_hill_climbing
	group by experimento, estrategia
)
order by obj desc;


--comparativa de malos, regulares y buenos, por experimento y estrategia
select
	coalesce(malos.experimento, regulares.experimento, buenos.experimento) experimento, 
	coalesce(malos.estrategia, regulares.estrategia, buenos.estrategia) estrategia, 
	coalesce(cant_malos, 0) cant_malos, 
	coalesce(cant_regulares, 0) cant_regulares, 
	coalesce(cant_buenos, 0) cant_buenos 
from (
	--cant malos por estrategia
	select experimento, estrategia, count(*) cant_malos
	from public.experimento_hill_climbing
	where obj < 3368093.624 and experimento = '100_it_all_x' 
	group by experimento, estrategia
) as malos

full join (
	--cant regulares por estrategia
	select experimento, estrategia, count(*) cant_regulares
	from public.experimento_hill_climbing
	where obj >= 6736187.248 and obj < 8420234.06 and experimento = '100_it_all_x' 
	group by experimento, estrategia
) as regulares
on malos.estrategia = regulares.estrategia

full join (
	--cant buenos por estrategia
	select experimento, estrategia, count(*) cant_buenos
	from public.experimento_hill_climbing
	where obj >= 8420234.06 and experimento = '100_it_all_x' 
	group by experimento, estrategia
) as buenos
on regulares.estrategia = buenos.estrategia
order by cant_buenos desc, cant_regulares desc, cant_malos;
