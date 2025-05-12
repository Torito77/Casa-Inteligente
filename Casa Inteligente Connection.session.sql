-- DROP TABLE det_lecturas;
-- DROP TABLE lecturas;
-- DROP TABLE sensores;
-- DROP TABLE actuadores;
-- DROP TABLE dispositivos;
-- DROP TABLE cuartos;
-- DROP TABLE tipos;

-- INSERT INTO cuartos (nombre, descripcion)
-- VALUES 
-- ('Sala principal','El area central de la casa'),
-- ('Cochera','Cochera, donde se encuentra la puerta automática'),
-- ('Entrada','La entrada de la casa');

-- INSERT INTO tipos (tipo)
-- VALUES
-- ('actuador'),
-- ('sensor');

-- INSERT INTO dispositivos (nombre,tipo_id,cuarto_id,fecha_instalacion)
-- VALUES
-- ('Sensor de ruido',2,1,NOW()),
-- ('Sensor de luz',2,1,NOW()),
-- ('Sensor de humedad',2,1,NOW()),
-- ('Sensor de temperatura',2,1,NOW()),
-- ('Puerta de cochera',1,2,NOW()),
-- ('Timbre',1,3,NOW());

-- INSERT INTO sensores (tipo_sensor, unidad_medida, dispositivo_id)
-- VALUES
-- ('RUIDO','dB',1),
-- ('LUZ','lux',2),
-- ('HUM','%',3),
-- ('TEMP','°C',4);

-- INSERT INTO actuadores (tipo_actuador, dispositivo_id)
-- VALUES
-- ('Servo',5),
-- ('Buzzer',6);

-- INSERT INTO lecturas (timestamp)
-- VALUES (NOW());

-- INSERT INTO det_lecturas (valor,lectura_id,sensor_id)
-- VALUES
-- (0,1,1),
-- (0,1,2),
-- (0,1,3),
-- (0,1,4);