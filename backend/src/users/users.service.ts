import { Injectable, NotFoundException, BadRequestException, InternalServerErrorException } from '@nestjs/common';
import { prisma } from 'src/prisma';
import { UserDto } from './dtos/user.dto';

@Injectable()
export class UsersService {

  async createUser(createUserDto: UserDto) {
    try {
      return await prisma.user.create({
        data: createUserDto,
      });
    } catch (error) {
      throw new BadRequestException('Erro ao criar usuário: ' + error.message);
    }
  }

  async getAllUsers() {
    try {
      return await prisma.user.findMany();
    } catch (error) {
      throw new InternalServerErrorException('Erro ao buscar usuários: ' + error.message);
    }
  }

  async getUserById(id: string) {
    try {
      const user = await prisma.user.findUnique({
        where: { user_id: Number(id) },
      });

      if (!user) {
        throw new NotFoundException(`Usuário com ID ${id} não encontrado`);
      }

      return user;
    } catch (error) {
      if (error instanceof NotFoundException) throw error;
      throw new InternalServerErrorException('Erro ao buscar usuário: ' + error.message);
    }
  }

  async updateUser(id: string, updateUserDto: UserDto) {
    try {
      const updatedUser = await prisma.user.update({
        where: { user_id: Number(id) },
        data: updateUserDto,
      });

      return updatedUser;
    } catch (error) {
      if (error.code === 'P2025') { // Prisma: registro não encontrado
        throw new NotFoundException(`Usuário com ID ${id} não encontrado`);
      }
      throw new BadRequestException('Erro ao atualizar usuário: ' + error.message);
    }
  }

  async deleteUser(id: string) {
    try {
      return await prisma.user.delete({
        where: { user_id: Number(id) },
      });
    } catch (error) {
      if (error.code === 'P2025') { // Prisma: registro não encontrado
        throw new NotFoundException(`Usuário com ID ${id} não encontrado`);
      }
      throw new BadRequestException('Erro ao deletar usuário: ' + error.message);
    }
  }

}
