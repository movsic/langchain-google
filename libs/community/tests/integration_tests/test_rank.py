import os
from unittest.mock import create_autospec

import pytest
from google.cloud import discoveryengine_v1alpha
from langchain.retrievers import ContextualCompressionRetriever
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore, VectorStoreRetriever

from langchain_google_community.rank.rank import VertexAIRank


class MockVectorStoreRetriever(VectorStoreRetriever):
    def _get_relevant_documents(self, query):
        return [
            Document(
                page_content="Life and career\nChildhood, youth and education\nSee also: Einstein family\nEinstein in 1882, age\xa03\nAlbert Einstein was born in Ulm,[19] in the Kingdom of Württemberg in the German Empire, on 14 March 1879.[20][21] His parents, secular Ashkenazi Jews, were Hermann Einstein, a salesman and engineer, and Pauline Koch. In 1880, the family moved to Munich's borough of Ludwigsvorstadt-Isarvorstadt, where Einstein's father and his uncle Jakob founded Elektrotechnische Fabrik J. Einstein & Cie, a company that manufactured electrical equipment based on direct current.[19]\nAlbert attended a Catholic elementary school in Munich from the age of five. When he was eight, he was transferred to the Luitpold Gymnasium, where he received advanced primary and then secondary school education.[22]",
                metadata={
                    "language": "en",
                    "source": "https://en.wikipedia.org/wiki/Albert_Einstein",
                    "title": "Albert Einstein - Wikipedia",
                },
            ),
            Document(
                page_content="A volume of Einstein's letters released by Hebrew University of Jerusalem in 2006[61] added further names to the catalog of women with whom he was romantically involved. They included Margarete Lebach (a married Austrian),[62] Estella Katzenellenbogen (the rich owner of a florist business), Toni Mendel (a wealthy Jewish widow) and Ethel Michanowski (a Berlin socialite), with whom he spent time and from whom he accepted gifts while married to Löwenthal.[63][64] After being widowed, Einstein was briefly in a relationship with Margarita Konenkova, thought by some to be a Russian spy; her husband, the Russian sculptor Sergei Konenkov, created the bronze bust of Einstein at the Institute for Advanced Study at Princeton.[65][66][failed verification]\nFollowing an episode of acute mental illness at about the age of twenty, Einstein's son Eduard was diagnosed with schizophrenia.[67] He spent the remainder of his life either in the care of his mother or in temporary confinement in an asylum. After her death, he was committed permanently to Burghölzli, the Psychiatric University Hospital in Zürich.[68]",
                metadata={
                    "language": "en",
                    "source": "https://en.wikipedia.org/wiki/Albert_Einstein",
                    "title": "Albert Einstein - Wikipedia",
                },
            ),
            Document(
                page_content='Marriages, relationships and children\nAlbert Einstein and Mileva Marić Einstein, 1912\nAlbert Einstein and Elsa Einstein, 1930\nCorrespondence between Einstein and Marić, discovered and published in 1987, revealed that in early 1902, while Marić was visiting her parents in Novi Sad, she gave birth to a daughter, Lieserl. When Marić returned to Switzerland it was without the child, whose fate is uncertain. A letter of Einstein\'s that he wrote in September 1903 suggests that the girl was either given up for adoption or died of scarlet fever in infancy.[45][46]\nEinstein and Marić married in January 1903. In May 1904, their son Hans Albert was born in Bern, Switzerland. Their son Eduard was born in Zürich in July 1910. In letters that Einstein wrote to Marie Winteler in the months before Eduard\'s arrival, he described his love for his wife as "misguided" and mourned the "missed life" that he imagined he would have enjoyed if he had married Winteler instead: "I think of you in heartfelt love every spare minute and am so unhappy as only a man can be."[47]',
                metadata={
                    "language": "en",
                    "source": "https://en.wikipedia.org/wiki/Albert_Einstein",
                    "title": "Albert Einstein - Wikipedia",
                },
            ),
        ]


@pytest.fixture
def mock_vector_store_retriever():
    mock_store = create_autospec(VectorStore, instance=True)
    return MockVectorStoreRetriever(vectorstore=mock_store)


@pytest.fixture
def rank_service_client():
    return (
        discoveryengine_v1alpha.RankServiceClient()
    )  # Ensure you have credentials configured


@pytest.fixture
def ranker(rank_service_client):
    return VertexAIRank(
        project_id=os.environ["PROJECT_ID"],
        location_id=os.environ["REGION"],
        ranking_config=os.environ["RANKING_CONFIG"],
        title_field="source",
        client=rank_service_client,
    )


def test_compression_retriever(mock_vector_store_retriever, ranker):
    print(mock_vector_store_retriever.get_relevant_documents("hi"))
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=ranker, base_retriever=mock_vector_store_retriever
    )
    query = "What was the name of einstein's mother ?"
    compressed_docs = compression_retriever.get_relevant_documents(query)

    expected_docs = [
        Document(
            page_content="Life and career\nChildhood, youth and education\nSee also: Einstein family\nEinstein in 1882, age\xa03\nAlbert Einstein was born in Ulm,[19] in the Kingdom of Württemberg in the German Empire, on 14 March 1879.[20][21] His parents, secular Ashkenazi Jews, were Hermann Einstein, a salesman and engineer, and Pauline Koch. In 1880, the family moved to Munich's borough of Ludwigsvorstadt-Isarvorstadt, where Einstein's father and his uncle Jakob founded Elektrotechnische Fabrik J. Einstein & Cie, a company that manufactured electrical equipment based on direct current.[19]\nAlbert attended a Catholic elementary school in Munich from the age of five. When he was eight, he was transferred to the Luitpold Gymnasium, where he received advanced primary and then secondary school education.[22]",
            metadata={
                "id": "0",
                "relevance_score": 0.7599999904632568,
                "source": "https://en.wikipedia.org/wiki/Albert_Einstein",
            },
        ),
        Document(
            page_content='Marriages, relationships and children\nAlbert Einstein and Mileva Marić Einstein, 1912\nAlbert Einstein and Elsa Einstein, 1930\nCorrespondence between Einstein and Marić, discovered and published in 1987, revealed that in early 1902, while Marić was visiting her parents in Novi Sad, she gave birth to a daughter, Lieserl. When Marić returned to Switzerland it was without the child, whose fate is uncertain. A letter of Einstein\'s that he wrote in September 1903 suggests that the girl was either given up for adoption or died of scarlet fever in infancy.[45][46]\nEinstein and Marić married in January 1903. In May 1904, their son Hans Albert was born in Bern, Switzerland. Their son Eduard was born in Zürich in July 1910. In letters that Einstein wrote to Marie Winteler in the months before Eduard\'s arrival, he described his love for his wife as "misguided" and mourned the "missed life" that he imagined he would have enjoyed if he had married Winteler instead: "I think of you in heartfelt love every spare minute and am so unhappy as only a man can be."[47]',
            metadata={
                "id": "2",
                "relevance_score": 0.6399999856948853,
                "source": "https://en.wikipedia.org/wiki/Albert_Einstein",
            },
        ),
        Document(
            page_content="A volume of Einstein's letters released by Hebrew University of Jerusalem in 2006[61] added further names to the catalog of women with whom he was romantically involved. They included Margarete Lebach (a married Austrian),[62] Estella Katzenellenbogen (the rich owner of a florist business), Toni Mendel (a wealthy Jewish widow) and Ethel Michanowski (a Berlin socialite), with whom he spent time and from whom he accepted gifts while married to Löwenthal.[63][64] After being widowed, Einstein was briefly in a relationship with Margarita Konenkova, thought by some to be a Russian spy; her husband, the Russian sculptor Sergei Konenkov, created the bronze bust of Einstein at the Institute for Advanced Study at Princeton.[65][66][failed verification]\nFollowing an episode of acute mental illness at about the age of twenty, Einstein's son Eduard was diagnosed with schizophrenia.[67] He spent the remainder of his life either in the care of his mother or in temporary confinement in an asylum. After her death, he was committed permanently to Burghölzli, the Psychiatric University Hospital in Zürich.[68]",
            metadata={
                "id": "1",
                "relevance_score": 0.10999999940395355,
                "source": "https://en.wikipedia.org/wiki/Albert_Einstein",
            },
        ),
    ]

    assert len(compressed_docs) == len(expected_docs)
    for doc, expected in zip(compressed_docs, expected_docs):
        assert doc.page_content == expected.page_content
        assert doc.metadata["id"] == expected.metadata["id"]
        assert float(doc.metadata.get("relevance_score", 0)) == pytest.approx(
            float(expected.metadata["relevance_score"])
        )
