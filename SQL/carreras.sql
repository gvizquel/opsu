SELECT
	im.nombre AS "institución",
	im.dep_admin AS dependencia_administrativa,
	l.nombre AS localidad,
	"c".nombre AS carrera,
	ac.nombre AS area_conocimiento,
	sac.nombre AS sub_area_conocimiento,
	CASE		
		WHEN C.cod_activacion = '11111111' OR C.cod_activacion = '10111111' THEN
			'activa' ELSE'inactiva' 
		END AS activa_inactiva,
	"c"."id" AS codigo_carrera 
FROM
	oeu.carrera AS "c"
	INNER JOIN oeu.localidad AS l ON "c".localidad_id = l."id"
	INNER JOIN oeu.ieu AS ieu ON l.ieu_id = ieu."id"
	INNER JOIN "public".institucion_ministerial AS im ON ieu.institucion_ministerial_id = im."id"
	INNER JOIN oeu.area_conocimiento ac ON "c".area_conocimiento_id = ac."id"
	INNER JOIN oeu.sub_area_conocimiento sac ON "c".sub_area_conocimiento_id = sac."id" 
ORDER BY
	im.nombre ASC,
l.nombre ASC,
"c".nombre ASC