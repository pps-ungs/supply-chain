create table experimento_neighborhood (
	id serial primary key,
	evaluation_strategy text not null,
	neighbor_strategy text not null,
	best_y numeric not null,
	num_neighbors int not null,
	num_iterations int not null,
	step int not null,
	time numeric not null,
);
