import { Controller, Get, Post, Patch, Delete, Param, Body, ParseIntPipe } from '@nestjs/common';
import { UsersService } from 'src/users/users.service';
import { UserDto } from 'src/users/dtos/user.dto';
import { ApiTags, ApiOperation, ApiResponse, ApiParam, ApiBody } from '@nestjs/swagger';

@ApiTags('Users')
@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Post('/create')
  @ApiOperation({ summary: 'Cria um novo usuário' })
  @ApiBody({ type: UserDto })
  @ApiResponse({ status: 201, description: 'Usuário criado com sucesso.' })
  @ApiResponse({ status: 400, description: 'Erro ao criar usuário.' })
  async createUser(@Body() user: UserDto) {
    return await this.usersService.createUser(user);
  }

  @Get('/list')
  @ApiOperation({ summary: 'Retorna todos os usuários' })
  @ApiResponse({ status: 200, description: 'Lista de usuários retornada com sucesso.' })
  @ApiResponse({ status: 500, description: 'Erro ao buscar usuários.' })
  async getAllUsers() {
    return await this.usersService.getAllUsers();
  }

  @Get('/:id')
  @ApiOperation({ summary: 'Retorna um usuário pelo ID' })
  @ApiParam({ name: 'id', description: 'ID do usuário', type: Number })
  @ApiResponse({ status: 200, description: 'Usuário encontrado com sucesso.' })
  @ApiResponse({ status: 404, description: 'Usuário não encontrado.' })
  async getUserById(@Param('id', ParseIntPipe) id: number) {
    return await this.usersService.getUserById(id.toString());
  }

  @Patch('/:id')
  @ApiOperation({ summary: 'Atualiza um usuário pelo ID' })
  @ApiParam({ name: 'id', description: 'ID do usuário', type: Number })
  @ApiBody({ type: UserDto })
  @ApiResponse({ status: 200, description: 'Usuário atualizado com sucesso.' })
  @ApiResponse({ status: 404, description: 'Usuário não encontrado.' })
  @ApiResponse({ status: 400, description: 'Erro ao atualizar usuário.' })
  async updateUser(@Param('id', ParseIntPipe) id: number, @Body() user: UserDto) {
    return await this.usersService.updateUser(id.toString(), user);
  }

  @Delete('/:id')
  @ApiOperation({ summary: 'Deleta um usuário pelo ID' })
  @ApiParam({ name: 'id', description: 'ID do usuário', type: Number })
  @ApiResponse({ status: 200, description: 'Usuário deletado com sucesso.' })
  @ApiResponse({ status: 404, description: 'Usuário não encontrado.' })
  @ApiResponse({ status: 400, description: 'Erro ao deletar usuário.' })
  async deleteUser(@Param('id', ParseIntPipe) id: number) {
    return await this.usersService.deleteUser(id.toString());
  }
}
