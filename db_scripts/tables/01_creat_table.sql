CREATE TABLE tbl_collections (
    id SERIAL PRIMARY KEY,
    collectionSetName VARCHAR(100) NOT NULL,
    releaseDate DATE NOT NULL,
    totalCardsInCollection SMALLINT NOT NULL
);

CREATE TABLE tbl_types (
    id SERIAL PRIMARY KEY,
    typeName VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE tbl_stages (
    id SERIAL PRIMARY KEY,
    stageName VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE tbl_cards (
    id SERIAL PRIMARY KEY,
    hp SMALLINT,
    name VARCHAR(80) NOT NULL,
    info TEXT,
    attack VARCHAR(100),
    damage VARCHAR(10),
    weak VARCHAR(20),
    ressis VARCHAR(20),
    retreat VARCHAR(20),
    cardNumberInCollection SMALLINT NOT NULL,
    collection_id INT NOT NULL,
    type_id INT NOT NULL,
    stage_id INT NOT NULL,
    CONSTRAINT fk_collection FOREIGN KEY (collection_id)
        REFERENCES tbl_collections (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_type FOREIGN KEY (type_id)
        REFERENCES tbl_types (id)
        ON DELETE RESTRICT,
    CONSTRAINT fk_stage FOREIGN KEY (stage_id)
        REFERENCES tbl_stages (id)
        ON DELETE RESTRICT
);
