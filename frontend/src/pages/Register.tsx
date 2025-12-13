import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Upload, ArrowLeft, UserPlus } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { countries } from '@/data/mockData';

export default function Register() {
  const [step, setStep] = useState<'form' | 'verify'>('form');
  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,hsl(185_95%_50%/0.1),transparent_50%)]" />
      <Card className="w-full max-w-md border-border/50 bg-card/80 backdrop-blur relative">
        <CardHeader className="text-center">
          <div className="mx-auto mb-4 w-16 h-16 rounded-full bg-destructive/20 flex items-center justify-center"><span className="text-4xl">🎈</span></div>
          <CardTitle className="text-3xl gradient-text">Criar Conta</CardTitle>
          <CardDescription>{step === 'form' ? 'Preencha seus dados' : 'Verifique seu email'}</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {step === 'form' ? (
            <>
              <div className="flex justify-center"><div className="w-20 h-20 rounded-full border-2 border-dashed border-border flex items-center justify-center cursor-pointer hover:border-primary transition-colors"><Upload className="h-6 w-6 text-muted-foreground" /></div></div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2"><Label>Nome</Label><Input placeholder="Seu nome" className="bg-background/50" /></div>
                <div className="space-y-2"><Label>Login</Label><Input placeholder="@seulogin" className="bg-background/50" /></div>
              </div>
              <div className="space-y-2"><Label>Email</Label><Input type="email" placeholder="seu@email.com" className="bg-background/50" /></div>
              <div className="space-y-2"><Label>País</Label><Select><SelectTrigger className="bg-background/50"><SelectValue placeholder="Selecione" /></SelectTrigger><SelectContent>{countries.map(c => <SelectItem key={c} value={c}>{c}</SelectItem>)}</SelectContent></Select></div>
              <div className="space-y-2"><Label>Senha</Label><Input type="password" placeholder="••••••••" className="bg-background/50" /></div>
            </>
          ) : (
            <div className="space-y-4 text-center">
              <p className="text-muted-foreground">Enviamos um código para seu email</p>
              <Input placeholder="Digite o código" className="bg-background/50 text-center text-2xl tracking-widest" maxLength={6} />
            </div>
          )}
        </CardContent>
        <CardFooter className="flex flex-col gap-3">
          {step === 'form' ? (
            <Button className="w-full" onClick={() => setStep('verify')}>Enviar Código de Verificação</Button>
          ) : (
            <Button className="w-full gap-2"><UserPlus className="h-4 w-4" />Registrar</Button>
          )}
          <Link to="/login" className="text-sm text-muted-foreground hover:text-foreground flex items-center gap-1"><ArrowLeft className="h-4 w-4" />Voltar para Login</Link>
        </CardFooter>
      </Card>
    </div>
  );
}
