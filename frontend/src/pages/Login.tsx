import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Eye, EyeOff, LogIn } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';

export default function Login() {
  const [showPassword, setShowPassword] = useState(false);
  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,hsl(270_95%_65%/0.1),transparent_50%)]" />
      <Card className="w-full max-w-md border-border/50 bg-card/80 backdrop-blur relative">
        <CardHeader className="text-center">
          <div className="mx-auto mb-4 w-16 h-16 rounded-full bg-destructive/20 flex items-center justify-center animate-pulse-slow">
            <span className="text-4xl">🎈</span>
          </div>
          <CardTitle className="text-3xl gradient-text">RedBalloon</CardTitle>
          <CardDescription>Entre na sua conta</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="login">Login ou Email</Label>
            <Input id="login" placeholder="seu@email.com" className="bg-background/50" />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Senha</Label>
            <div className="relative">
              <Input id="password" type={showPassword ? 'text' : 'password'} placeholder="••••••••" className="bg-background/50 pr-10" />
              <Button type="button" variant="ghost" size="icon" className="absolute right-0 top-0 h-full" onClick={() => setShowPassword(!showPassword)}>
                {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </Button>
            </div>
          </div>
        </CardContent>
        <CardFooter className="flex flex-col gap-3">
          <Link to="/home" className="w-full">
            <Button className="w-full gap-2"><LogIn className="h-4 w-4" />Entrar</Button>
          </Link>
          <div className="flex gap-4 text-sm">
            <Link to="/register" className="text-primary hover:underline">Cadastrar-se</Link>
            <button className="text-muted-foreground hover:text-foreground">Recuperar Senha</button>
          </div>
        </CardFooter>
      </Card>
    </div>
  );
}
