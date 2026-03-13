import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Upload, ArrowLeft, UserPlus } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'

import { countries } from '@/data/mockData'
import AvatarSeeds from '@/types/avatars'

export default function Register() {
  const [step, setStep] = useState<'form' | 'verify'>('form')
  const [avatarModalOpen, setAvatarModalOpen] = useState(false)
  const [avatarSeed, setAvatarSeed] = useState<string>(AvatarSeeds[0])

  const avatarUrl = (seed: string) =>
    `https://api.dicebear.com/9.x/adventurer/svg?seed=${seed}`

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,hsl(270_90%_60%/0.08),transparent_55%)]" />

      <Card className="w-full max-w-md border-border/50 bg-card/80 backdrop-blur relative">
        <CardHeader className="text-center">
          <div
            className="mx-auto mb-4 w-20 h-20 rounded-full border-2 border-dashed border-border
                       flex items-center justify-center cursor-pointer hover:border-primary transition"
            onClick={() => setAvatarModalOpen(true)}
          >
            <img
              src={avatarUrl(avatarSeed)}
              alt="Avatar"
              className="w-16 h-16 rounded-full"
            />
          </div>

          <CardTitle className="text-3xl gradient-text">
            Criar Conta
          </CardTitle>
          <CardDescription>
            {step === 'form' ? 'Preencha seus dados' : 'Verifique seu email'}
          </CardDescription>
        </CardHeader>

        <CardContent className="space-y-4">
          {step === 'form' ? (
            <>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Nome</Label>
                  <Input placeholder="Seu nome" className="bg-background/50" />
                </div>
                <div className="space-y-2">
                  <Label>Login</Label>
                  <Input placeholder="@seulogin" className="bg-background/50" />
                </div>
              </div>

              <div className="space-y-2">
                <Label>Email</Label>
                <Input
                  type="email"
                  placeholder="seu@email.com"
                  className="bg-background/50"
                />
              </div>

              <div className="space-y-2">
                <Label>País</Label>
                <Select>
                  <SelectTrigger className="bg-background/50">
                    <SelectValue placeholder="Selecione" />
                  </SelectTrigger>
                  <SelectContent>
                    {countries.map(c => (
                      <SelectItem key={c} value={c}>
                        {c}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Senha</Label>
                <Input
                  type="password"
                  placeholder="••••••••"
                  className="bg-background/50"
                />
              </div>
            </>
          ) : (
            <div className="space-y-4 text-center">
              <p className="text-muted-foreground">
                Enviamos um código para seu email
              </p>
              <Input
                placeholder="000000"
                className="bg-background/50 text-center text-2xl tracking-widest"
                maxLength={6}
              />
            </div>
          )}
        </CardContent>

        <CardFooter className="flex flex-col gap-3">
          {step === 'form' ? (
            <Button className="w-full" onClick={() => setStep('verify')}>
              Enviar Código de Verificação
            </Button>
          ) : (
            <Button className="w-full gap-2">
              <UserPlus className="h-4 w-4" />
              Registrar
            </Button>
          )}

          <Link
            to="/login"
            className="text-sm text-muted-foreground hover:text-foreground flex items-center gap-1"
          >
            <ArrowLeft className="h-4 w-4" />
            Voltar para Login
          </Link>
        </CardFooter>
      </Card>

      {/* AVATAR MODAL */}
      <Dialog open={avatarModalOpen} onOpenChange={setAvatarModalOpen}>
        <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Escolha seu avatar</DialogTitle>
          </DialogHeader>

          <div className="grid grid-cols-6 gap-4 mt-4">
            {AvatarSeeds.map(seed => (
              <button
                key={seed}
                onClick={() => {
                  setAvatarSeed(seed)
                  setAvatarModalOpen(false)
                }}
                className={`
                  rounded-full p-1 transition flex items-center justify-center
                  border border-white/15 bg-white/5
                  ${
                    avatarSeed === seed
                      ? 'ring-2 ring-primary border-primary/60'
                      : 'hover:border-white/30 hover:bg-white/10'
                  }
                `}
              >
                <img
                  src={avatarUrl(seed)}
                  alt={seed}
                  className="w-15 h-15 rounded-full"
                />
              </button>
            ))}
          </div>
        </DialogContent>
      </Dialog>

    </div>
  )
}
