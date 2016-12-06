SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `coffeerhythm` ;
CREATE SCHEMA IF NOT EXISTS `coffeerhythm` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
SHOW WARNINGS;
USE `coffeerhythm` ;

-- -----------------------------------------------------
-- Table `coffeerhythm`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `coffeerhythm`.`user` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `coffeerhythm`.`user` (
  `email` VARCHAR(50) NOT NULL ,
  `password` VARCHAR(50) NOT NULL ,
  `nickname` VARCHAR(50) NOT NULL ,
  `avatar` VARCHAR(200) NOT NULL ,
  `introduction` TEXT NULL ,
  `city` VARCHAR(50) NULL ,
  `created_at` DOUBLE NOT NULL ,
  `isadmin` TINYINT(1) NOT NULL ,
  `enjoy_sugar` TINYINT(1) NOT NULL ,
  `enjoy_milk` TINYINT(1) NOT NULL ,
  `single_espresso` TINYINT(1) NOT NULL ,
  PRIMARY KEY (`email`) )
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `coffeerhythm`.`cafe`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `coffeerhythm`.`cafe` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `coffeerhythm`.`cafe` (
  `email` VARCHAR(50) NOT NULL ,
  `password` VARCHAR(50) NOT NULL ,
  `image` VARCHAR(200) NOT NULL ,
  `name` VARCHAR(50) NOT NULL ,
  `city` VARCHAR(50) NOT NULL ,
  `address` VARCHAR(200) NOT NULL ,
  `introduction` TEXT NULL ,
  PRIMARY KEY (`email`) )
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `coffeerhythm`.`activity`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `coffeerhythm`.`activity` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `coffeerhythm`.`activity` (
  `idactivity` VARCHAR(50) NOT NULL ,
  `start_at` DOUBLE NOT NULL ,
  `end_at` DOUBLE NOT NULL ,
  `image` VARCHAR(200) NOT NULL ,
  `name` VARCHAR(50) NOT NULL ,
  `introduction` TEXT NOT NULL ,
  `belong_to` VARCHAR(50) NULL ,
  `created_from` VARCHAR(50) NULL ,
  `address` VARCHAR(200) NOT NULL ,
  `signup_start_at` DOUBLE NOT NULL ,
  `signup_end_at` DOUBLE NOT NULL ,
  PRIMARY KEY (`idactivity`) ,
  INDEX `belong_to_idx` (`belong_to` ASC) ,
  CONSTRAINT `activity_belong_to`
    FOREIGN KEY (`belong_to` )
    REFERENCES `coffeerhythm`.`cafe` (`email` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `coffeerhythm`.`course`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `coffeerhythm`.`course` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `coffeerhythm`.`course` (
  `idcourse` VARCHAR(50) NOT NULL ,
  `image` VARCHAR(200) NOT NULL ,
  `name` TEXT NOT NULL ,
  `author` VARCHAR(50) NOT NULL ,
  `created_at` DOUBLE NOT NULL ,
  `introduction` TEXT NULL ,
  `video` VARCHAR(200) NOT NULL ,
  `israwbest` TINYINT(1) NOT NULL ,
  PRIMARY KEY (`idcourse`) ,
  INDEX `course_author_idx` (`author` ASC) ,
  CONSTRAINT `course_author`
    FOREIGN KEY (`author` )
    REFERENCES `coffeerhythm`.`user` (`email` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `coffeerhythm`.`article`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `coffeerhythm`.`article` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `coffeerhythm`.`article` (
  `idarticle` VARCHAR(50) NOT NULL ,
  `image` VARCHAR(200) NOT NULL ,
  `name` TEXT NOT NULL ,
  `author` VARCHAR(50) NOT NULL ,
  `created_at` DOUBLE NOT NULL ,
  `content` VARCHAR(200) NOT NULL ,
  `family` VARCHAR(50) NULL ,
  `isknowledge` TINYINT(1) NOT NULL ,
  `isnote` TINYINT(1) NOT NULL ,
  `isdemand` TINYINT(1) NOT NULL ,
  `about_cafe` VARCHAR(50) NULL ,
  `about_course` VARCHAR(50) NULL ,
  `about_drink` TINYINT(1) NULL ,
  PRIMARY KEY (`idarticle`) ,
  INDEX `about_idx` (`about_cafe` ASC) ,
  INDEX `author_idx` (`author` ASC) ,
  INDEX `article_about_course_idx` (`about_course` ASC) ,
  CONSTRAINT `article_about_cafe`
    FOREIGN KEY (`about_cafe` )
    REFERENCES `coffeerhythm`.`cafe` (`email` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `article_author`
    FOREIGN KEY (`author` )
    REFERENCES `coffeerhythm`.`user` (`email` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `article_about_course`
    FOREIGN KEY (`about_course` )
    REFERENCES `coffeerhythm`.`course` (`idcourse` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `coffeerhythm`.`comment_article`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `coffeerhythm`.`comment_article` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `coffeerhythm`.`comment_article` (
  `idcomment_article` VARCHAR(50) NOT NULL ,
  `created_from` VARCHAR(50) NOT NULL ,
  `reply_to` VARCHAR(50) NULL ,
  `created_at` DOUBLE NOT NULL ,
  `content` TEXT NOT NULL ,
  `about` VARCHAR(50) NOT NULL ,
  PRIMARY KEY (`idcomment_article`) ,
  INDEX `created_from_idx` (`created_from` ASC) ,
  INDEX `reply_to_idx` (`reply_to` ASC) ,
  INDEX `about_idx` (`about` ASC) ,
  CONSTRAINT `comment_article_created_from`
    FOREIGN KEY (`created_from` )
    REFERENCES `coffeerhythm`.`user` (`email` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `comment_article_reply_to`
    FOREIGN KEY (`reply_to` )
    REFERENCES `coffeerhythm`.`comment_article` (`idcomment_article` )
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `comment_article_about`
    FOREIGN KEY (`about` )
    REFERENCES `coffeerhythm`.`article` (`idarticle` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `coffeerhythm`.`collect_article`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `coffeerhythm`.`collect_article` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `coffeerhythm`.`collect_article` (
  `user` VARCHAR(50) NOT NULL ,
  `article` VARCHAR(50) NOT NULL ,
  `created_at` DOUBLE NOT NULL ,
  PRIMARY KEY (`user`, `article`) ,
  INDEX `_user_idx` (`user` ASC) ,
  INDEX `_article_idx` (`article` ASC) ,
  CONSTRAINT `collect_article_user`
    FOREIGN KEY (`user` )
    REFERENCES `coffeerhythm`.`user` (`email` )
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `collect_article_article`
    FOREIGN KEY (`article` )
    REFERENCES `coffeerhythm`.`article` (`idarticle` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `coffeerhythm`.`like_article`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `coffeerhythm`.`like_article` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `coffeerhythm`.`like_article` (
  `user` VARCHAR(50) NOT NULL ,
  `article` VARCHAR(50) NOT NULL ,
  `created_at` DOUBLE NOT NULL ,
  PRIMARY KEY (`user`, `article`) ,
  INDEX `_user_idx` (`user` ASC) ,
  INDEX `_article_idx` (`article` ASC) ,
  CONSTRAINT `like_article_user`
    FOREIGN KEY (`user` )
    REFERENCES `coffeerhythm`.`user` (`email` )
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `like_article_article`
    FOREIGN KEY (`article` )
    REFERENCES `coffeerhythm`.`article` (`idarticle` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `coffeerhythm`.`coffee`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `coffeerhythm`.`coffee` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `coffeerhythm`.`coffee` (
  `name` VARCHAR(50) NOT NULL ,
  PRIMARY KEY (`name`) )
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `coffeerhythm`.`follow`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `coffeerhythm`.`follow` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `coffeerhythm`.`follow` (
  `fromwho` VARCHAR(50) NOT NULL ,
  `towho` VARCHAR(50) NOT NULL ,
  `created_at` DOUBLE NOT NULL ,
  PRIMARY KEY (`fromwho`, `towho`) ,
  INDEX `_fromwho_idx` (`fromwho` ASC) ,
  INDEX `_towho_idx` (`towho` ASC) ,
  CONSTRAINT `follow_fromwho`
    FOREIGN KEY (`fromwho` )
    REFERENCES `coffeerhythm`.`user` (`email` )
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `follow_towho`
    FOREIGN KEY (`towho` )
    REFERENCES `coffeerhythm`.`user` (`email` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `coffeerhythm`.`have_coffee`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `coffeerhythm`.`have_coffee` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `coffeerhythm`.`have_coffee` (
  `cafe` VARCHAR(50) NOT NULL ,
  `coffee` VARCHAR(50) NOT NULL ,
  PRIMARY KEY (`cafe`, `coffee`) ,
  INDEX `_idcafe_idx` (`cafe` ASC) ,
  INDEX `_coffee_idx` (`coffee` ASC) ,
  CONSTRAINT `have_coffee_cafe`
    FOREIGN KEY (`cafe` )
    REFERENCES `coffeerhythm`.`cafe` (`email` )
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `have_coffee_coffee`
    FOREIGN KEY (`coffee` )
    REFERENCES `coffeerhythm`.`coffee` (`name` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `coffeerhythm`.`enjoy`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `coffeerhythm`.`enjoy` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `coffeerhythm`.`enjoy` (
  `user` VARCHAR(50) NOT NULL ,
  `coffee` VARCHAR(50) NOT NULL ,
  PRIMARY KEY (`user`, `coffee`) ,
  INDEX `_user_idx` (`user` ASC) ,
  INDEX `_coffee_idx` (`coffee` ASC) ,
  CONSTRAINT `enjoy_user`
    FOREIGN KEY (`user` )
    REFERENCES `coffeerhythm`.`user` (`email` )
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `enjoy_coffee`
    FOREIGN KEY (`coffee` )
    REFERENCES `coffeerhythm`.`coffee` (`name` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `coffeerhythm`.`join`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `coffeerhythm`.`join` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `coffeerhythm`.`join` (
  `user` VARCHAR(50) NOT NULL ,
  `activity` VARCHAR(50) NOT NULL ,
  `created_at` DOUBLE NOT NULL ,
  PRIMARY KEY (`user`, `activity`) ,
  INDEX `_user_idx` (`user` ASC) ,
  INDEX `_activity_idx` (`activity` ASC) ,
  CONSTRAINT `join_user`
    FOREIGN KEY (`user` )
    REFERENCES `coffeerhythm`.`user` (`email` )
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `join_activity`
    FOREIGN KEY (`activity` )
    REFERENCES `coffeerhythm`.`activity` (`idactivity` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `coffeerhythm`.`like_cafe`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `coffeerhythm`.`like_cafe` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `coffeerhythm`.`like_cafe` (
  `user` VARCHAR(50) NOT NULL ,
  `cafe` VARCHAR(50) NOT NULL ,
  `created_at` DOUBLE NOT NULL ,
  PRIMARY KEY (`user`, `cafe`) ,
  INDEX `_user_idx` (`user` ASC) ,
  INDEX `_cafe_idx` (`cafe` ASC) ,
  CONSTRAINT `like_cafe_user`
    FOREIGN KEY (`user` )
    REFERENCES `coffeerhythm`.`user` (`email` )
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `like_cafe_cafe`
    FOREIGN KEY (`cafe` )
    REFERENCES `coffeerhythm`.`cafe` (`email` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `coffeerhythm`.`comment_cafe`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `coffeerhythm`.`comment_cafe` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `coffeerhythm`.`comment_cafe` (
  `idcomment_cafe` VARCHAR(50) NOT NULL ,
  `created_from` VARCHAR(50) NOT NULL ,
  `reply_to` VARCHAR(50) NULL ,
  `created_at` DOUBLE NOT NULL ,
  `content` TEXT NOT NULL ,
  `about` VARCHAR(50) NOT NULL ,
  PRIMARY KEY (`idcomment_cafe`) ,
  INDEX `_created_from_idx` (`created_from` ASC) ,
  INDEX `_reply_to_idx` (`reply_to` ASC) ,
  INDEX `_about_idx` (`about` ASC) ,
  CONSTRAINT `comment_cafe_created_from`
    FOREIGN KEY (`created_from` )
    REFERENCES `coffeerhythm`.`user` (`email` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `comment_cafe_reply_to`
    FOREIGN KEY (`reply_to` )
    REFERENCES `coffeerhythm`.`comment_cafe` (`idcomment_cafe` )
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
  CONSTRAINT `comment_cafe_about`
    FOREIGN KEY (`about` )
    REFERENCES `coffeerhythm`.`cafe` (`email` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `coffeerhythm`.`collect_cafe`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `coffeerhythm`.`collect_cafe` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `coffeerhythm`.`collect_cafe` (
  `user` VARCHAR(50) NOT NULL ,
  `cafe` VARCHAR(50) NOT NULL ,
  `created_at` DOUBLE NOT NULL ,
  PRIMARY KEY (`user`, `cafe`) ,
  INDEX `_user_idx` (`user` ASC) ,
  INDEX `_cafe_idx` (`cafe` ASC) ,
  CONSTRAINT `collect_cafe_user`
    FOREIGN KEY (`user` )
    REFERENCES `coffeerhythm`.`user` (`email` )
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `collect_cafe_cafe`
    FOREIGN KEY (`cafe` )
    REFERENCES `coffeerhythm`.`cafe` (`email` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `coffeerhythm`.`collect_activity`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `coffeerhythm`.`collect_activity` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `coffeerhythm`.`collect_activity` (
  `user` VARCHAR(50) NOT NULL ,
  `activity` VARCHAR(50) NOT NULL ,
  `created_at` DOUBLE NOT NULL ,
  PRIMARY KEY (`user`, `activity`) ,
  INDEX `_user_idx` (`user` ASC) ,
  INDEX `_activity_idx` (`activity` ASC) ,
  CONSTRAINT `collect_activity_user`
    FOREIGN KEY (`user` )
    REFERENCES `coffeerhythm`.`user` (`email` )
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `collect_activity_activity`
    FOREIGN KEY (`activity` )
    REFERENCES `coffeerhythm`.`activity` (`idactivity` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `coffeerhythm`.`note_tag`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `coffeerhythm`.`note_tag` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `coffeerhythm`.`note_tag` (
  `name` VARCHAR(50) NOT NULL ,
  PRIMARY KEY (`name`) )
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `coffeerhythm`.`have_note_tag`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `coffeerhythm`.`have_note_tag` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `coffeerhythm`.`have_note_tag` (
  `note` VARCHAR(50) NOT NULL ,
  `tag` VARCHAR(50) NOT NULL ,
  PRIMARY KEY (`note`, `tag`) ,
  INDEX `_article_idx` (`note` ASC) ,
  INDEX `_tag_idx` (`tag` ASC) ,
  CONSTRAINT `have_note_tag_note`
    FOREIGN KEY (`note` )
    REFERENCES `coffeerhythm`.`article` (`idarticle` )
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `have_note_tag_tag`
    FOREIGN KEY (`tag` )
    REFERENCES `coffeerhythm`.`note_tag` (`name` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `coffeerhythm`.`course_tag`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `coffeerhythm`.`course_tag` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `coffeerhythm`.`course_tag` (
  `name` VARCHAR(50) NOT NULL ,
  PRIMARY KEY (`name`) )
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `coffeerhythm`.`have_course_tag`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `coffeerhythm`.`have_course_tag` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `coffeerhythm`.`have_course_tag` (
  `course` VARCHAR(50) NOT NULL ,
  `tag` VARCHAR(50) NOT NULL ,
  PRIMARY KEY (`course`, `tag`) ,
  INDEX `have_course_tag_course_idx` (`course` ASC) ,
  INDEX `have_course_tag_tag_idx` (`tag` ASC) ,
  CONSTRAINT `have_course_tag_course`
    FOREIGN KEY (`course` )
    REFERENCES `coffeerhythm`.`course` (`idcourse` )
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `have_course_tag_tag`
    FOREIGN KEY (`tag` )
    REFERENCES `coffeerhythm`.`course_tag` (`name` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `coffeerhythm`.`read`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `coffeerhythm`.`read` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `coffeerhythm`.`read` (
  `user` VARCHAR(50) NOT NULL ,
  `article` VARCHAR(50) NOT NULL ,
  PRIMARY KEY (`user`, `article`) ,
  INDEX `read_user_idx` (`user` ASC) ,
  INDEX `read_article_idx` (`article` ASC) ,
  CONSTRAINT `read_user`
    FOREIGN KEY (`user` )
    REFERENCES `coffeerhythm`.`user` (`email` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `read_article`
    FOREIGN KEY (`article` )
    REFERENCES `coffeerhythm`.`article` (`idarticle` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `coffeerhythm`.`look`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `coffeerhythm`.`look` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `coffeerhythm`.`look` (
  `user` VARCHAR(50) NOT NULL ,
  `course` VARCHAR(50) NOT NULL ,
  PRIMARY KEY (`user`, `course`) ,
  INDEX `look_user_idx` (`user` ASC) ,
  INDEX `look_course_idx` (`course` ASC) ,
  CONSTRAINT `look_user`
    FOREIGN KEY (`user` )
    REFERENCES `coffeerhythm`.`user` (`email` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `look_course`
    FOREIGN KEY (`course` )
    REFERENCES `coffeerhythm`.`course` (`idcourse` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `coffeerhythm`.`comment_course`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `coffeerhythm`.`comment_course` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `coffeerhythm`.`comment_course` (
  `idcomment_course` VARCHAR(50) NOT NULL ,
  `created_from` VARCHAR(50) NOT NULL ,
  `reply_to` VARCHAR(50) NULL ,
  `created_at` DOUBLE NOT NULL ,
  `content` TEXT NOT NULL ,
  `about` VARCHAR(50) NOT NULL ,
  PRIMARY KEY (`idcomment_course`) ,
  INDEX `comment_course_created_from_idx` (`created_from` ASC) ,
  INDEX `comment_course_reply_to_idx` (`reply_to` ASC) ,
  INDEX `comment_course_about_idx` (`about` ASC) ,
  CONSTRAINT `comment_course_created_from`
    FOREIGN KEY (`created_from` )
    REFERENCES `coffeerhythm`.`user` (`email` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `comment_course_reply_to`
    FOREIGN KEY (`reply_to` )
    REFERENCES `coffeerhythm`.`comment_course` (`idcomment_course` )
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `comment_course_about`
    FOREIGN KEY (`about` )
    REFERENCES `coffeerhythm`.`course` (`idcourse` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `coffeerhythm`.`collect_course`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `coffeerhythm`.`collect_course` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `coffeerhythm`.`collect_course` (
  `user` VARCHAR(50) NOT NULL ,
  `course` VARCHAR(50) NOT NULL ,
  `created_at` DOUBLE NOT NULL ,
  PRIMARY KEY (`user`, `course`) ,
  INDEX `collect_course_user_idx` (`user` ASC) ,
  INDEX `collect_course_course_idx` (`course` ASC) ,
  CONSTRAINT `collect_course_user`
    FOREIGN KEY (`user` )
    REFERENCES `coffeerhythm`.`user` (`email` )
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `collect_course_course`
    FOREIGN KEY (`course` )
    REFERENCES `coffeerhythm`.`course` (`idcourse` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `coffeerhythm`.`like_course`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `coffeerhythm`.`like_course` ;

SHOW WARNINGS;
CREATE  TABLE IF NOT EXISTS `coffeerhythm`.`like_course` (
  `user` VARCHAR(50) NOT NULL ,
  `course` VARCHAR(50) NOT NULL ,
  `created_at` DOUBLE NOT NULL ,
  PRIMARY KEY (`user`, `course`) ,
  INDEX `like_course_user_idx` (`user` ASC) ,
  INDEX `like_course_course_idx` (`course` ASC) ,
  CONSTRAINT `like_course_user`
    FOREIGN KEY (`user` )
    REFERENCES `coffeerhythm`.`user` (`email` )
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `like_course_course`
    FOREIGN KEY (`course` )
    REFERENCES `coffeerhythm`.`course` (`idcourse` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;
USE `coffeerhythm` ;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
