import { useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, Mail, Key, Check } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { InputOTP, InputOTPGroup, InputOTPSlot } from '@/components/ui/input-otp';
import { useToast } from '@/hooks/use-toast';

export default function Recover() {
  const [step, setStep] = useState<'email' | 'code' | 'password'>('email');
  const [email, setEmail] = useState('');
  const [code, setCode] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();

  const handleSendCode = () => {
    if (!email) return;
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setStep('code');
      toast({ title: 'Código enviado!', description: 'Verifique seu e-mail.' });
    }, 1500);
  };

  const handleVerifyCode = () => {
    if (code.length < 6) return;
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setStep('password');
      toast({ title: 'Código verificado!', description: 'Agora defina sua nova senha.' });
    }, 1500);
  };

  const handleResetPassword = () => {
    if (password !== confirmPassword) {
      toast({ title: 'Erro', description: 'As senhas não coincidem.', variant: 'destructive' });
      return;
    }
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      toast({ title: 'Senha alterada!', description: 'Você já pode fazer login.' });
    }, 1500);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-background">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,hsl(var(--neon-purple)/0.15),transparent_50%)]" />
      
      <Card className="w-full max-w-md arcade-card relative z-10">
        <CardHeader className="text-center">
          <Link to="/login" className="absolute left-4 top-4">
            <Button variant="ghost" size="icon"><ArrowLeft className="h-4 w-4" /></Button>
          </Link>
          <div className="mx-auto mb-4 w-16 h-16 rounded-full bg-gradient-to-br from-[hsl(var(--neon-purple))] to-[hsl(var(--neon-pink))] flex items-center justify-center neon-glow">
            {step === 'email' && <Mail className="h-8 w-8 text-white" />}
            {step === 'code' && <Key className="h-8 w-8 text-white" />}
            {step === 'password' && <Check className="h-8 w-8 text-white" />}
          </div>
          <CardTitle className="text-2xl font-bold" style={{ fontFamily: 'Orbitron, sans-serif' }}>
            {step === 'email' && 'Recuperar Senha'}
            {step === 'code' && 'Verificar Código'}
            {step === 'password' && 'Nova Senha'}
          </CardTitle>
          <CardDescription>
            {step === 'email' && 'Digite seu e-mail para receber o código'}
            {step === 'code' && 'Digite o código enviado para seu e-mail'}
            {step === 'password' && 'Defina sua nova senha'}
          </CardDescription>
        </CardHeader>
        
        <CardContent className="space-y-4">
          {step === 'email' && (
            <>
              <div className="space-y-2">
                <Label>E-mail</Label>
                <Input 
                  type="email" 
                  placeholder="seu@email.com" 
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="bg-input"
                />
              </div>
              <Button 
                onClick={handleSendCode} 
                disabled={loading || !email}
                className="w-full arcade-button"
              >
                {loading ? 'Enviando...' : 'Enviar Código'}
              </Button>
            </>
          )}

          {step === 'code' && (
            <>
              <div className="space-y-2">
                <Label>Código de Verificação</Label>
                <div className="flex justify-center">
                  <InputOTP maxLength={6} value={code} onChange={setCode}>
                    <InputOTPGroup>
                      <InputOTPSlot index={0} />
                      <InputOTPSlot index={1} />
                      <InputOTPSlot index={2} />
                      <InputOTPSlot index={3} />
                      <InputOTPSlot index={4} />
                      <InputOTPSlot index={5} />
                    </InputOTPGroup>
                  </InputOTP>
                </div>
              </div>
              <Button 
                onClick={handleVerifyCode} 
                disabled={loading || code.length < 6}
                className="w-full arcade-button"
              >
                {loading ? 'Verificando...' : 'Verificar'}
              </Button>
              <Button variant="ghost" onClick={() => setStep('email')} className="w-full">
                Reenviar código
              </Button>
            </>
          )}

          {step === 'password' && (
            <>
              <div className="space-y-2">
                <Label>Nova Senha</Label>
                <Input 
                  type="password" 
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="bg-input"
                />
              </div>
              <div className="space-y-2">
                <Label>Confirmar Senha</Label>
                <Input 
                  type="password" 
                  placeholder="••••••••"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="bg-input"
                />
              </div>
              <Button 
                onClick={handleResetPassword} 
                disabled={loading || !password || !confirmPassword}
                className="w-full arcade-button"
              >
                {loading ? 'Salvando...' : 'Alterar Senha'}
              </Button>
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
