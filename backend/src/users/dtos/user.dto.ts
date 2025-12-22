import { ApiProperty } from "@nestjs/swagger";
import { IsNotEmpty, IsDate, IsEmail, IsNumber, IsOptional, IsString, MaxLength } from "class-validator";
import { Type, Transform } from "class-transformer";

export class UserDto {

    @ApiProperty({ example: "joaozinho", description: "Nome de usuário" })
    @IsString()
    @MaxLength(300)
    @IsNotEmpty()
    name: string;

    @ApiProperty({ example: "joao.12", description: "Nickname do usuário" })
    @IsString()
    @MaxLength(150)
    @IsNotEmpty()
    nickname: string;

    @ApiProperty({ example: "@349@49!0483", description: "Senha do usuário (hash)" })
    @IsString()
    @MaxLength(300)
    @IsNotEmpty()
    password: string;

    @ApiProperty({ example: "joao@gmail.com", description: "Email do usuário" })
    @IsEmail()
    @MaxLength(255)
    @IsNotEmpty()
    email: string;

    @ApiProperty({ example: "avatar1.png", description: "Avatar do usuário" })
    @IsString()
    @MaxLength(200)
    avatar: string;

    @ApiProperty({ example: "Um estudante apaixonado por programação.", description: "Descrição do usuário" })
    @IsString()
    @MaxLength(250)
    @IsOptional()
    description?: string;

    @ApiProperty({ example: "Brazil", description: "Nacionalidade" })
    @IsString()
    @MaxLength(100)
    nationality: string;

    @ApiProperty({ example: "2024-12-24T00:00:00.000Z", description: "Data de criação do usuário" })
    @IsOptional()
    @Type(() => Date)
    @IsDate()
    @Transform(({ value }) => value ?? new Date())
    created_at?: Date;
}