-- Seed collections
INSERT INTO tbl_collections (collectionSetName, releaseDate, totalCardsInCollection)
VALUES 
('Base Set', '1999-01-09', 102),
('Jungle', '1999-06-16', 64),
('Fossil', '1999-10-10', 62);

-- Seed types
INSERT INTO tbl_types (typeName)
VALUES 
('Fire'),
('Water'),
('Grass'),
('Electric'),
('Psychic'),
('Fighting'),
('Dark'),
('Steel'),
('Dragon'),
('Fairy'),
('Colorless');

-- Seed stages
INSERT INTO tbl_stages (stageName)
VALUES 
('Basic'),
('Stage 1'),
('Stage 2');

-- Seed cards
INSERT INTO tbl_cards (hp, name, info, attack, damage, weak, ressis, retreat, cardNumberInCollection, collection_id, type_id, stage_id)
VALUES
(120, 'Charizard', 'Flame Pokémon', 'Fire Spin', '100', 'Water', 'None', '3 Colorless', 4, 1, 1, 3),
(60, 'Pikachu', 'Mouse Pokémon', 'Thunder Jolt', '30', 'Fighting', 'Steel', '1 Colorless', 58, 1, 4, 1),
(90, 'Venusaur', 'Seed Pokémon', 'Solar Beam', '60', 'Fire', 'Water', '2 Colorless', 15, 1, 3, 3),
(80, 'Scyther', 'Mantis Pokémon', 'Slash', '30', 'Fire', 'Fighting', '1 Colorless', 10, 2, 3, 1),
(70, 'Lapras', 'Transport Pokémon', 'Water Gun', '30+', 'Electric', 'None', '2 Colorless', 10, 3, 2, 1);
