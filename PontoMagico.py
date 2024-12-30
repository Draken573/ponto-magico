import click
import pandas as pd
import os
import datetime
from openpyxl import load_workbook


def identify_batidas(row):
    if isinstance(row, str):
        batidas = row.split(' ')
        return len(batidas)
    return 0


def extract_day_of_week(text):
    if isinstance(text, str):
        parts = text.split(' ')
        if len(parts) > 1:
            return parts[-1]
    return ''


def extract_justificativa(text):
    if isinstance(text, str):
        parts = text.split(' - ')
        if len(parts) > 1:
            justificativa = parts[1].split(' |')[0].strip()
            justificativa = justificativa.replace('BH', '').strip()
            return justificativa
    return ''


def extract_date(text):
    if isinstance(text, str):
        parts = text.split(' ')
        return parts[0]
    return None


def extract_time_columns(row, num_batidas):
    if isinstance(row, str):
        batidas = row.split(' ')
        if len(batidas) == num_batidas:
            return batidas
    return [None] * num_batidas


def extract_and_split_batidas(row):
    if isinstance(row, str):
        batidas = row.split(' ')
        num_batidas = len(batidas)

        separated_batidas = [None, None, None, None]
        current_index = 0

        for i in range(num_batidas):
            if current_index < 4:
                if '-' in batidas[i]:
                    horas = batidas[i].split('-')
                    for hora in horas:
                        if current_index < 4:
                            separated_batidas[current_index] = hora
                            current_index += 1
                else:
                    separated_batidas[current_index] = batidas[i]
                    current_index += 1

        return pd.Series(separated_batidas, index=['Batida 1', 'Batida 2', 'Batida 3', 'Batida 4'])

    return pd.Series([None] * 4, index=['Batida 1', 'Batida 2', 'Batida 3', 'Batida 4'])


@click.command()
@click.option('--input', prompt='Caminho da planilha de entrada',
              help='Caminho para a planilha de entrada')
def main(input):
    click.secho("Bem-vindo ao Ponto Mágico!", fg='green')

    input = os.path.abspath(input)
    output_folder = os.path.join(os.getcwd(), 'tratamentos')

    if not input.endswith('.xlsx'):
        click.secho("O arquivo de entrada deve estar no formato .xlsx.", fg='red')
        return

    click.echo(f"Carregando a planilha de {input}...")

    try:
        # Ler a planilha ignorando as linhas de cabeçalho
        df = pd.read_excel(input, header=6)
    except Exception as e:
        click.secho(f"Erro ao carregar a planilha: {e}", fg='red')
        return

    # Atualizar a lista de colunas a serem mantidas
    columns_to_keep = [
        'Nome da Pessoa', 'Matrícula', 'Estrutura organizacional', 
        'Data da Marcação', 'Horário', 'Descontos', 
        'Banco de horas Débito', 'Banco de horas Crédito', 
        'Justificativa', 'Observação', 'Marcações'
    ]
    
    existing_columns = [col for col in df.columns if any(keep in col for keep in columns_to_keep)]
    
    if not existing_columns:
        click.secho("Colunas necessárias não encontradas na planilha.", fg='red')
        print("Colunas disponíveis:", df.columns)
        return

    df = df[existing_columns]

    click.echo("Planilha carregada. Verificando as primeiras linhas...")
    print(df.head(6))

    click.echo("Realizando tratamentos nos dados...")

    # Tratamento 1: Separar data e dia da semana
    df['Dia da Semana'] = df['Data da Marcação'].apply(extract_day_of_week)
    df['Data da Marcação'] = df['Data da Marcação'].apply(extract_date)

    # Tratamento 3: Separar e preencher as colunas de batidas
    df_batidas = df['Marcações'].apply(extract_and_split_batidas)
    df = pd.concat([df, df_batidas], axis=1)

    # Tratamento 4: Limpar justificativa
    if 'Justificativa' in df.columns:
        df['Justificativa'] = df['Justificativa'].apply(extract_justificativa)

    # Verifica se as colunas "Batida 2" e "Batida 3" estão presentes
    if 'Batida 2' not in df.columns or 'Batida 3' not in df.columns:
        click.secho("As colunas 'Batida 2' e 'Batida 3' não foram encontradas na planilha.", fg='red')
        return

    # Tratamento 2: Calcular colunas "Intrajornada" e "Carga Horária"
    df['Intrajornada'] = pd.to_datetime(df['Batida 3']) - pd.to_datetime(df['Batida 2'])
    df['Carga Horária'] = pd.to_datetime(df['Batida 4']) - pd.to_datetime(df['Batida 1']) - df['Intrajornada']

    # Formatação das colunas de tempo
    df['Intrajornada'] = df['Intrajornada'].apply(
        lambda x: f"{x.seconds//3600:02d}:{(x.seconds//60)%60:02d}" if pd.notna(x) else '')
    df['Carga Horária'] = df['Carga Horária'].apply(
        lambda x: f"{x.seconds//3600:02d}:{(x.seconds//60)%60:02d}" if pd.notna(x) else '')

    current_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs(output_folder, exist_ok=True)
    output = os.path.join(output_folder, f"nova_planilha_{current_date}.xlsx")

    if 'Marcações' in df.columns:
        df.drop(columns=['Marcações'], inplace=True)
    
    df.to_excel(output, index=False, engine='openpyxl')

    click.secho("Tratamento concluído! A nova planilha foi salva com sucesso.", fg='green')


if __name__ == '__main__':
    main()