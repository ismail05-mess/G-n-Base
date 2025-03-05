CREATE TABLE IF NOT EXISTS "Departement" (
	"nom_departement" varchar(100) NOT NULL,
	"id_departement" bigint NOT NULL UNIQUE,
	PRIMARY KEY ("id_departement")
);

CREATE TABLE IF NOT EXISTS "Commune" (
	"id_commune" serial NOT NULL UNIQUE,
	"nom_commune" varchar(100) NOT NULL,
	"id_departement" bigint NOT NULL,
	PRIMARY KEY ("id_commune")
);

CREATE TABLE IF NOT EXISTS "Type_Acte" (
	"id_type_acte" serial NOT NULL UNIQUE,
	"libelle" varchar(100) NOT NULL,
	PRIMARY KEY ("id_type_acte")
);

CREATE TABLE IF NOT EXISTS "Personne" (
	"id_personne" uuid NOT NULL UNIQUE,
	"nom" varchar(100) NOT NULL,
	"prenom" varchar(100) NOT NULL,
	"prenom_pere" varchar(100) NOT NULL,
	"nom_mere" varchar(100) NOT NULL,
	"prenom_mere" varchar(100) NOT NULL,
	PRIMARY KEY ("id_personne")
);

CREATE TABLE IF NOT EXISTS "Acte" (
	"id_acte" serial NOT NULL UNIQUE,
	"date_acte" date NOT NULL,
	"num_vue" varchar(50) NOT NULL,
	"id_type_acte" bigint NOT NULL,
	"id_commune" bigint NOT NULL,
	"id_personne_A" uuid NOT NULL,
	"id_personne_B" uuid NOT NULL,
	PRIMARY KEY ("id_acte")
);


ALTER TABLE "Commune" ADD CONSTRAINT "Commune_fk2" FOREIGN KEY ("id_departement") REFERENCES "Departement"("id_departement");


ALTER TABLE "Acte" ADD CONSTRAINT "Acte_fk3" FOREIGN KEY ("id_type_acte") REFERENCES "Type_Acte"("id_type_acte");

ALTER TABLE "Acte" ADD CONSTRAINT "Acte_fk4" FOREIGN KEY ("id_commune") REFERENCES "Commune"("id_commune");

ALTER TABLE "Acte" ADD CONSTRAINT "Acte_fk5" FOREIGN KEY ("id_personne_A") REFERENCES "Personne"("id_personne");

ALTER TABLE "Acte" ADD CONSTRAINT "Acte_fk6" FOREIGN KEY ("id_personne_B") REFERENCES "Personne"("id_personne");