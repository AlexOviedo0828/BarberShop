-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema barbershop_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema barbershop_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `barbershop_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `barbershop_db` ;

-- -----------------------------------------------------
-- Table `barbershop_db`.`categorias`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `barbershop_db`.`categorias` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `barbershop_db`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `barbershop_db`.`usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100) NOT NULL,
  `apellido` VARCHAR(100) NOT NULL,
  `email` VARCHAR(150) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `rol` ENUM('admin', 'usuario') NULL DEFAULT 'usuario',
  `telefono` VARCHAR(20) NULL DEFAULT NULL,
  `fecha_registro` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email` (`email` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 9
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `barbershop_db`.`peluqueros`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `barbershop_db`.`peluqueros` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100) NOT NULL,
  `apellido` VARCHAR(100) NOT NULL,
  `disponible` TINYINT NOT NULL DEFAULT '0',
  `especialidad` VARCHAR(100) NULL DEFAULT NULL,
  `telefono` VARCHAR(20) NULL DEFAULT NULL,
  `imagen` VARCHAR(255) NULL DEFAULT NULL,
  `servicios_realizados` INT NULL DEFAULT '0',
  `fecha_creacion` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `barbershop_db`.`citas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `barbershop_db`.`citas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `usuario_id` INT NOT NULL,
  `peluquero_id` INT NOT NULL,
  `fecha` DATE NOT NULL,
  `hora` TIME NOT NULL,
  `estado` ENUM('pendiente', 'confirmada', 'cancelada', 'completada') NULL DEFAULT 'pendiente',
  `notas` TEXT NULL DEFAULT NULL,
  `duracion_minutos` INT NULL DEFAULT '30',
  PRIMARY KEY (`id`),
  INDEX `usuario_id` (`usuario_id` ASC) VISIBLE,
  INDEX `peluquero_id` (`peluquero_id` ASC) VISIBLE,
  CONSTRAINT `citas_ibfk_1`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `barbershop_db`.`usuarios` (`id`),
  CONSTRAINT `citas_ibfk_2`
    FOREIGN KEY (`peluquero_id`)
    REFERENCES `barbershop_db`.`peluqueros` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `barbershop_db`.`pedidos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `barbershop_db`.`pedidos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `usuario_id` INT NOT NULL,
  `peluquero_id` INT NULL DEFAULT NULL,
  `fecha` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `total` DECIMAL(10,2) NOT NULL,
  `estado` ENUM('pendiente', 'pagado', 'cancelado') NULL DEFAULT 'pendiente',
  `direccion_envio` VARCHAR(255) NULL DEFAULT NULL,
  `estado_despacho` ENUM('pendiente', 'en_camino', 'entregado', 'no_aplica') NULL DEFAULT 'no_aplica',
  `metodo_pago` VARCHAR(50) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `usuario_id` (`usuario_id` ASC) VISIBLE,
  INDEX `peluquero_id` (`peluquero_id` ASC) VISIBLE,
  CONSTRAINT `pedidos_ibfk_1`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `barbershop_db`.`usuarios` (`id`),
  CONSTRAINT `pedidos_ibfk_2`
    FOREIGN KEY (`peluquero_id`)
    REFERENCES `barbershop_db`.`peluqueros` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `barbershop_db`.`productos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `barbershop_db`.`productos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(150) NOT NULL,
  `descripcion` TEXT NULL DEFAULT NULL,
  `precio` DECIMAL(10,2) NOT NULL,
  `stock` INT NULL DEFAULT '0',
  `imagen` VARCHAR(255) NULL DEFAULT NULL,
  `categoria_id` INT NULL DEFAULT NULL,
  `ventas` INT NULL DEFAULT '0',
  `fecha_creacion` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `categoria_id` (`categoria_id` ASC) VISIBLE,
  CONSTRAINT `productos_ibfk_1`
    FOREIGN KEY (`categoria_id`)
    REFERENCES `barbershop_db`.`categorias` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `barbershop_db`.`detalles_pedido`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `barbershop_db`.`detalles_pedido` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `pedido_id` INT NOT NULL,
  `producto_id` INT NOT NULL,
  `cantidad` INT NOT NULL,
  `precio` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `pedido_id` (`pedido_id` ASC) VISIBLE,
  INDEX `producto_id` (`producto_id` ASC) VISIBLE,
  CONSTRAINT `detalles_pedido_ibfk_1`
    FOREIGN KEY (`pedido_id`)
    REFERENCES `barbershop_db`.`pedidos` (`id`),
  CONSTRAINT `detalles_pedido_ibfk_2`
    FOREIGN KEY (`producto_id`)
    REFERENCES `barbershop_db`.`productos` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `barbershop_db`.`historial_peluquero`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `barbershop_db`.`historial_peluquero` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `peluquero_id` INT NOT NULL,
  `pedido_id` INT NOT NULL,
  `descripcion` VARCHAR(255) NULL DEFAULT NULL,
  `fecha` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `peluquero_id` (`peluquero_id` ASC) VISIBLE,
  INDEX `pedido_id` (`pedido_id` ASC) VISIBLE,
  CONSTRAINT `historial_peluquero_ibfk_1`
    FOREIGN KEY (`peluquero_id`)
    REFERENCES `barbershop_db`.`peluqueros` (`id`),
  CONSTRAINT `historial_peluquero_ibfk_2`
    FOREIGN KEY (`pedido_id`)
    REFERENCES `barbershop_db`.`pedidos` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `barbershop_db`.`horarios_barbero`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `barbershop_db`.`horarios_barbero` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `barbero_id` INT NOT NULL,
  `dia` ENUM('lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado') NOT NULL,
  `reservado` TINYINT NOT NULL DEFAULT '0',
  `hora_inicio` TIME NOT NULL,
  `hora_fin` TIME NOT NULL,
  `descanso_inicio` TIME NULL DEFAULT NULL,
  `descanso_fin` TIME NULL DEFAULT NULL,
  `creado_en` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `barbero_id` (`barbero_id` ASC) VISIBLE,
  CONSTRAINT `horarios_barbero_ibfk_1`
    FOREIGN KEY (`barbero_id`)
    REFERENCES `barbershop_db`.`peluqueros` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
