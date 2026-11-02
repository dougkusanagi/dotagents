# Controle de pulo em jogos de plataforma

Aplique em jogos de plataforma com controlador de personagem próprio. Se a engine ou o projeto já tem um controlador com estes recursos, configure-o em vez de reescrever. Meça os tempos em segundos, não em frames, para não depender da taxa de quadros; os valores abaixo são padrões ajustáveis.

1. **Coyote time.** O jogador costuma apertar pulo logo depois de sair da borda; para ele, ainda estava nela. Aceite o pulo por cerca de 0,1 s (6 frames a 60 fps) depois de o personagem sair do chão, se ele não pulou nesse intervalo.
2. **Jump buffering.** Ao encadear pulos, o jogador aperta pulo logo antes de tocar o chão. Guarde o comando por cerca de 0,1 s e execute o pulo no frame em que o personagem tocar o chão.
3. **Corner correction.** Um pulo que erra a borda por poucos pixels bate na parede e escorrega, embora pareça ter alcançado. Se os pés ficarem até 4 px abaixo do topo da borda, empurre o personagem para cima dela. Aplique o mesmo ao bater a cabeça na quina de um teto: desloque-o na horizontal até 4 px para liberar o pulo.
